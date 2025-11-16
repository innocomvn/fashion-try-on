"""
Pydantic models for Fashion Try-On API
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ModelProvider(str, Enum):
    """Model provider enum"""
    ON_PREMISE = "on_premise"
    REPLICATE = "replicate"
    FAL = "fal"
    HEYBEAUTY = "heybeauty"


class GarmentCategory(str, Enum):
    """Garment category"""
    UPPERBODY = "upperbody"
    LOWERBODY = "lowerbody"
    DRESS = "dress"


# ============= Request Models =============

class TryOnRequest(BaseModel):
    """Try-on request model"""
    model_image_url: Optional[str] = Field(None, description="URL of model/person image")
    garment_image_url: Optional[str] = Field(None, description="URL of garment image")
    provider: ModelProvider = Field(ModelProvider.ON_PREMISE, description="Model provider to use")
    category: GarmentCategory = Field(GarmentCategory.UPPERBODY, description="Garment category")
    denoise_steps: int = Field(30, ge=10, le=50, description="Number of denoising steps")
    seed: int = Field(42, description="Random seed for reproducibility")
    auto_crop: bool = Field(True, description="Auto crop and align person image")
    auto_mask: bool = Field(True, description="Auto generate garment mask")

    @validator('model_image_url', 'garment_image_url')
    def validate_urls(cls, v):
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('URL must start with http:// or https://')
        return v


class TryOnResponse(BaseModel):
    """Try-on response model"""
    task_id: str = Field(..., description="Unique task ID")
    status: TaskStatus = Field(..., description="Task status")
    message: str = Field(..., description="Status message")
    result_url: Optional[str] = Field(None, description="Result image URL")
    created_at: datetime = Field(default_factory=datetime.now)


class TaskStatusResponse(BaseModel):
    """Task status query response"""
    task_id: str
    status: TaskStatus
    progress: int = Field(0, ge=0, le=100, description="Progress percentage")
    message: str
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    processing_time: Optional[float] = None  # in seconds


# ============= Database Models =============

class TryOnTaskDB(BaseModel):
    """Database model for try-on tasks"""
    id: int
    task_id: str
    model_image_path: str
    garment_image_path: str
    result_image_path: Optional[str] = None
    provider: str
    category: str
    status: str
    error_message: Optional[str] = None
    denoise_steps: int
    seed: int
    created_at: datetime
    updated_at: datetime
    processing_time: Optional[float] = None

    class Config:
        from_attributes = True


# ============= Health Check =============

class HealthCheck(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    on_premise_available: bool
    external_api_available: bool
    timestamp: datetime = Field(default_factory=datetime.now)
