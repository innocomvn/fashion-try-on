"""
File utilities for image handling
"""

import os
import uuid
import aiofiles
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

from backend.config import settings


async def save_upload_file(upload_file: UploadFile, directory: str) -> str:
    """
    Save uploaded file and return the file path

    Args:
        upload_file: FastAPI UploadFile object
        directory: Directory to save the file

    Returns:
        str: Path to saved file
    """
    # Validate file extension
    file_ext = Path(upload_file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(directory, unique_filename)

    # Read and validate file size
    content = await upload_file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
        )

    # Validate that it's a valid image
    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)

    return file_path


async def validate_and_preprocess_image(image_path: str, target_size: Tuple[int, int] = None) -> str:
    """
    Validate and optionally resize image

    Args:
        image_path: Path to image file
        target_size: Optional target size (width, height)

    Returns:
        str: Path to processed image (same as input if no processing)
    """
    try:
        image = Image.open(image_path)

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
            image.save(image_path)

        # Resize if target size specified
        if target_size:
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            image.save(image_path)

        return image_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


def delete_file(file_path: str) -> None:
    """Delete file if exists"""
    if os.path.exists(file_path):
        os.remove(file_path)


def get_file_url(file_path: str, base_url: str) -> str:
    """
    Convert file path to URL

    Args:
        file_path: Local file path
        base_url: Base URL of the server

    Returns:
        str: Full URL to file
    """
    # Extract relative path from full path
    relative_path = file_path.replace(os.getcwd() + "/", "")
    return f"{base_url}/{relative_path}"
