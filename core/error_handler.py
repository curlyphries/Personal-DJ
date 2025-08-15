"""
Error handling module for the Personal DJ application.
Provides consistent error tracking, logging, and handling throughout the application.
"""
import os
import sys
import traceback
from enum import Enum
from typing import Dict, Any, Optional, Union
from loguru import logger


class ErrorLevel(Enum):
    """Error severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DJError(Exception):
    """Base error class for Personal DJ application"""
    def __init__(self, 
                 message: str, 
                 level: ErrorLevel = ErrorLevel.ERROR, 
                 details: Optional[Dict[str, Any]] = None, 
                 original_error: Optional[Exception] = None):
        self.message = message
        self.level = level
        self.details = details or {}
        self.original_error = original_error
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for API responses"""
        result = {
            "error": self.__class__.__name__,
            "message": self.message,
            "level": self.level.value
        }
        
        if self.details:
            result["details"] = self.details
            
        if self.original_error:
            result["original_error"] = str(self.original_error)
            
        return result


class AudioPlaybackError(DJError):
    """Raised when there's an issue with audio playback"""
    pass


class TTSError(DJError):
    """Raised when text-to-speech service fails"""
    pass


class LLMError(DJError):
    """Raised when LLM service fails"""
    pass


class ConfigurationError(DJError):
    """Raised when there's a configuration issue"""
    pass


class FileOperationError(DJError):
    """Raised when file operations fail"""
    pass


# Configure logger
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {extra}"
LOG_PATH = os.getenv("LOG_PATH", "./logs/personal_dj.log")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Configure Loguru
logger.remove()  # Remove default handler
logger.add(sys.stderr, format=LOG_FORMAT, level=LOG_LEVEL)
logger.add(LOG_PATH, rotation="10 MB", retention="1 week", level=LOG_LEVEL)


def handle_exception(error: Union[DJError, Exception], context: Optional[str] = None) -> Dict[str, Any]:
    """Centralized exception handler that logs the error and returns a consistent response format"""
    if not isinstance(error, DJError):
        # Convert standard exceptions to DJError
        original_error = error
        error = DJError(
            message=str(error),
            level=ErrorLevel.ERROR,
            details={"exception_type": error.__class__.__name__},
            original_error=original_error
        )
    
    # Add exception traceback to details
    error.details["traceback"] = traceback.format_exc()
    
    # Add context if provided
    if context:
        error.details["context"] = context
    
    # Log the error with appropriate level
    log_message = f"{error.message}"
    if context:
        log_message = f"[{context}] {log_message}"
    
    if error.level == ErrorLevel.INFO:
        logger.info(log_message, extra=error.details)
    elif error.level == ErrorLevel.WARNING:
        logger.warning(log_message, extra=error.details)
    elif error.level == ErrorLevel.ERROR:
        logger.error(log_message, extra=error.details)
    elif error.level == ErrorLevel.CRITICAL:
        logger.critical(log_message, extra=error.details)
    
    return error.to_dict()
