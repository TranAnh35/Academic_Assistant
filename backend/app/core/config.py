# core/config.py
import os
import dotenv
from pydantic_settings import BaseSettings
import logging
import pathlib
from typing import Optional

CORE_DIR = pathlib.Path(__file__).resolve().parent
APP_DIR = CORE_DIR.parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

logger = logging.getLogger(__name__)

dotenv_path = APP_DIR / '.env'
if dotenv_path.is_file():
    dotenv.load_dotenv(dotenv_path=dotenv_path)
    logger.info(f"Loaded environment variables from: {dotenv_path}")
else:
    logger.warning(f".env file not found at expected location: {dotenv_path}")

_default_logs_dir_path = BACKEND_DIR.joinpath("logs").resolve()
_default_logs_dir_str = str(_default_logs_dir_path)

print(f"Default logs directory string: {_default_logs_dir_str}")

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "GeminiAcademicAssistant")
    
    LOGS_DIR: str = _default_logs_dir_str
    
    GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")
    GOOGLE_GENAI_USE_VERTEXAI: bool = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
    
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    class Config:
        env_file_encoding = 'utf-8'
        arbitrary_types_allowed = True
        extra='ignore'

settings = Settings()

print(f"LOGS_DIR: {settings.LOGS_DIR}")
logger.info(f"Using LOGS_DIR: {settings.LOGS_DIR}")