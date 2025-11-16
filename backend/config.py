"""
Configuration file for Fashion Try-On Backend
Supports both on-premise models and external API services
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Fashion Try-On Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # File Storage
    UPLOAD_DIR: str = "uploads"
    RESULT_DIR: str = "results"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png"}

    # Database (SQLite for simplicity, can be changed to PostgreSQL)
    DATABASE_URL: str = "sqlite:///./fashion_tryon.db"

    # ============= PHƯƠNG ÁN 1: ON-PREMISE MODEL =============
    # Model settings
    USE_ON_PREMISE: bool = True
    MODEL_TYPE: str = "idm-vton"  # Options: "idm-vton", "ootdiffusion", "outfitanyone"
    MODEL_PATH: str = "./models"
    DEVICE: str = "cuda"  # "cuda" or "cpu"

    # IDM-VTON settings
    IDM_VTON_CHECKPOINT: str = "./models/idm-vton"
    IDM_VTON_DENOISE_STEPS: int = 30
    IDM_VTON_SEED: int = 42

    # OOTDiffusion settings
    OOTD_CHECKPOINT: str = "./models/ootdiffusion"
    OOTD_MODEL_TYPE: str = "hd"  # "hd" or "dc"
    OOTD_CATEGORY: str = "upperbody"  # "upperbody", "lowerbody", "dress"

    # ============= PHƯƠNG ÁN 2: EXTERNAL API =============
    # API Provider Selection
    USE_EXTERNAL_API: bool = True
    API_PROVIDER: str = "replicate"  # Options: "replicate", "fal", "heybeauty"

    # HeyBeauty API (from existing code)
    HEYBEAUTY_API_URL: Optional[str] = None
    HEYBEAUTY_OPEN_ID: Optional[str] = None
    HEYBEAUTY_API_KEY: Optional[str] = None
    HEYBEAUTY_OSS_URL: Optional[str] = None

    # Replicate API - Kolors Virtual Try-On
    REPLICATE_API_TOKEN: Optional[str] = None
    REPLICATE_MODEL: str = "cuuupid/idm-vton:c871bb9b046607b680449ecbae55fd8c6d945e0a1948644bf2361b3d021d3ff4"

    # Fal.ai API - Try-On Diffusion
    FAL_API_KEY: Optional[str] = None
    FAL_MODEL: str = "fal-ai/idm-vton"

    # API Timeout settings
    API_TIMEOUT: int = 300  # 5 minutes
    API_MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create required directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULT_DIR, exist_ok=True)
os.makedirs(settings.MODEL_PATH, exist_ok=True)
