"""
Fashion Try-On Backend API
Supports both on-premise models and external API services

Author: Claude
Version: 1.0.0
"""

import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.config import settings
from backend.models.schemas import (
    TryOnRequest, TryOnResponse, TaskStatusResponse,
    HealthCheck, TaskStatus, ModelProvider
)
from backend.utils.database import db
from backend.utils.file_utils import save_upload_file, get_file_url
from backend.services.on_premise_service import get_on_premise_service
from backend.services.external_api_service import get_external_api_service


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Virtual Try-On API with on-premise and external API support",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=settings.RESULT_DIR), name="results")


# ============= Background Task Processing =============

async def process_tryon_task(
    task_id: str,
    model_image_path: str,
    garment_image_path: str,
    provider: str,
    category: str,
    denoise_steps: int,
    seed: int
):
    """
    Background task to process virtual try-on
    """
    try:
        # Update status to processing
        db.update_task(task_id, {'status': TaskStatus.PROCESSING.value})

        # Generate output path
        output_filename = f"{task_id}.jpg"
        output_path = os.path.join(settings.RESULT_DIR, output_filename)

        # Process based on provider
        if provider == ModelProvider.ON_PREMISE.value:
            service = get_on_premise_service()
            result = service.process_tryon(
                model_image_path=model_image_path,
                garment_image_path=garment_image_path,
                output_path=output_path,
                category=category,
                denoise_steps=denoise_steps,
                seed=seed
            )
        else:
            # External API providers
            service = get_external_api_service(provider)
            result = service.process_tryon(
                model_image_path=model_image_path,
                garment_image_path=garment_image_path,
                output_path=output_path,
                category=category,
                denoise_steps=denoise_steps
            )

        # Update task based on result
        if result['success']:
            db.update_task(task_id, {
                'status': TaskStatus.COMPLETED.value,
                'result_image_path': output_path,
                'processing_time': result.get('processing_time', 0)
            })
        else:
            db.update_task(task_id, {
                'status': TaskStatus.FAILED.value,
                'error_message': result.get('error', 'Unknown error'),
                'processing_time': result.get('processing_time', 0)
            })

    except Exception as e:
        db.update_task(task_id, {
            'status': TaskStatus.FAILED.value,
            'error_message': str(e)
        })


# ============= API Endpoints =============

@app.get("/", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint
    """
    return HealthCheck(
        status="healthy",
        version=settings.APP_VERSION,
        on_premise_available=settings.USE_ON_PREMISE,
        external_api_available=settings.USE_EXTERNAL_API
    )


@app.post("/api/v1/tryon", response_model=TryOnResponse)
async def create_tryon_task(
    background_tasks: BackgroundTasks,
    model_image: UploadFile = File(..., description="Model/Person image"),
    garment_image: UploadFile = File(..., description="Garment/Clothing image"),
    provider: str = Form(ModelProvider.ON_PREMISE.value, description="Provider: on_premise, replicate, fal, heybeauty"),
    category: str = Form("upperbody", description="Category: upperbody, lowerbody, dress"),
    denoise_steps: int = Form(30, description="Denoising steps (10-50)"),
    seed: int = Form(42, description="Random seed")
):
    """
    Create a new virtual try-on task

    **PHƯƠNG ÁN 1 (On-Premise)**: Set provider="on_premise"
    - Uses local models: IDM-VTON, OOTDiffusion, OutfitAnyone
    - Faster for local deployment
    - Requires GPU for best performance

    **PHƯƠNG ÁN 2 (External API)**: Set provider to "replicate", "fal", or "heybeauty"
    - Uses cloud API services
    - No GPU required
    - Requires API keys in .env file
    """
    try:
        # Generate task ID
        task_id = str(uuid.uuid4())

        # Save uploaded files
        model_image_path = await save_upload_file(model_image, settings.UPLOAD_DIR)
        garment_image_path = await save_upload_file(garment_image, settings.UPLOAD_DIR)

        # Create task in database
        task_data = {
            'task_id': task_id,
            'model_image_path': model_image_path,
            'garment_image_path': garment_image_path,
            'provider': provider,
            'category': category,
            'status': TaskStatus.PENDING.value,
            'denoise_steps': denoise_steps,
            'seed': seed
        }
        db.create_task(task_data)

        # Add background task
        background_tasks.add_task(
            process_tryon_task,
            task_id=task_id,
            model_image_path=model_image_path,
            garment_image_path=garment_image_path,
            provider=provider,
            category=category,
            denoise_steps=denoise_steps,
            seed=seed
        )

        return TryOnResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            message=f"Task created successfully using {provider} provider. Processing in background...",
            created_at=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tryon/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get status of a virtual try-on task
    """
    task = db.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Calculate progress
    progress = 0
    if task['status'] == TaskStatus.PENDING.value:
        progress = 0
    elif task['status'] == TaskStatus.PROCESSING.value:
        progress = 50
    elif task['status'] == TaskStatus.COMPLETED.value:
        progress = 100
    elif task['status'] == TaskStatus.FAILED.value:
        progress = 0

    # Generate result URL if completed
    result_url = None
    if task['status'] == TaskStatus.COMPLETED.value and task['result_image_path']:
        result_url = f"/results/{os.path.basename(task['result_image_path'])}"

    return TaskStatusResponse(
        task_id=task['task_id'],
        status=TaskStatus(task['status']),
        progress=progress,
        message=f"Task is {task['status']}",
        result_url=result_url,
        error_message=task.get('error_message'),
        created_at=datetime.fromisoformat(task['created_at']),
        updated_at=datetime.fromisoformat(task['updated_at']),
        processing_time=task.get('processing_time')
    )


@app.get("/api/v1/tryon/{task_id}/result")
async def download_result(task_id: str):
    """
    Download result image
    """
    task = db.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task['status'] != TaskStatus.COMPLETED.value:
        raise HTTPException(status_code=400, detail=f"Task is {task['status']}, not completed yet")

    if not task['result_image_path'] or not os.path.exists(task['result_image_path']):
        raise HTTPException(status_code=404, detail="Result image not found")

    return FileResponse(
        task['result_image_path'],
        media_type="image/jpeg",
        filename=f"tryon_{task_id}.jpg"
    )


@app.get("/api/v1/tasks")
async def list_tasks(limit: int = 100, offset: int = 0):
    """
    List all tasks
    """
    tasks = db.list_tasks(limit=limit, offset=offset)
    return {
        "total": len(tasks),
        "tasks": tasks
    }


@app.delete("/api/v1/tryon/{task_id}")
async def delete_task(task_id: str):
    """
    Delete a task and its files
    """
    task = db.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete files
    if os.path.exists(task['model_image_path']):
        os.remove(task['model_image_path'])
    if os.path.exists(task['garment_image_path']):
        os.remove(task['garment_image_path'])
    if task['result_image_path'] and os.path.exists(task['result_image_path']):
        os.remove(task['result_image_path'])

    # Delete from database
    db.delete_task(task_id)

    return {"message": "Task deleted successfully"}


# ============= Main =============

if __name__ == "__main__":
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║           Fashion Try-On Backend API v{settings.APP_VERSION}           ║
    ╚═══════════════════════════════════════════════════════════╝

    🚀 Starting server...
    📍 Host: {settings.HOST}:{settings.PORT}
    📚 Docs: http://{settings.HOST}:{settings.PORT}/docs

    ⚙️  Configuration:
    - On-Premise: {'✅ Enabled' if settings.USE_ON_PREMISE else '❌ Disabled'}
    - External API: {'✅ Enabled' if settings.USE_EXTERNAL_API else '❌ Disabled'}
    - API Provider: {settings.API_PROVIDER}

    """)

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
