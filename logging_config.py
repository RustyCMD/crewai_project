"""
Centralized Logging Configuration for CrewAI Project
Provides consistent logging setup across all modules with proper Unicode support
"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SafeFormatter(logging.Formatter):
    """Custom formatter that handles Unicode characters safely"""
    
    def format(self, record):
        try:
            # Try normal formatting first
            return super().format(record)
        except UnicodeEncodeError:
            # If Unicode error, replace problematic characters
            record.msg = str(record.msg).encode('ascii', 'replace').decode('ascii')
            if record.args:
                safe_args = []
                for arg in record.args:
                    if isinstance(arg, str):
                        safe_args.append(arg.encode('ascii', 'replace').decode('ascii'))
                    else:
                        safe_args.append(arg)
                record.args = tuple(safe_args)
            return super().format(record)

class CrewAILogger:
    """Centralized logger configuration for CrewAI project"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.setup_logging()
            self._initialized = True
    
    def setup_logging(self):
        """Set up comprehensive logging configuration"""
        
        # Get configuration from environment
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        log_file = os.getenv('LOG_FILE', './logs/crewai_game_dev.log')
        
        # Ensure log level is valid
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            log_level = 'INFO'
        
        # Create logs directory
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
        
        # Clear existing handlers to avoid conflicts
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create handlers list
        handlers = []
        
        # File handler with rotation
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level))
            
            # Use safe formatter for file output
            file_formatter = SafeFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            handlers.append(file_handler)
            
        except Exception as e:
            print(f"Warning: Could not create file handler: {e}")
        
        # Console handler with safe encoding
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_level))
            
            # Use safe formatter for console output
            console_formatter = SafeFormatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            handlers.append(console_handler)
            
        except Exception as e:
            print(f"Warning: Could not create console handler: {e}")
        
        # Configure root logger
        if handlers:
            logging.basicConfig(
                level=getattr(logging, log_level),
                handlers=handlers,
                force=True
            )
        else:
            # Fallback configuration
            logging.basicConfig(
                level=getattr(logging, log_level),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                force=True
            )
        
        # Log successful initialization
        logger = logging.getLogger(__name__)
        logger.info("CrewAI logging system initialized")
        logger.info(f"Log level: {log_level}")
        logger.info(f"Log file: {log_file}")
        
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with the given name"""
        return logging.getLogger(name)
    
    def log_safe(self, logger: logging.Logger, level: str, message: str, *args, **kwargs):
        """Log a message with safe Unicode handling"""
        try:
            # Replace common problematic Unicode characters with safe alternatives
            safe_message = self._make_message_safe(message)
            safe_args = []
            
            for arg in args:
                if isinstance(arg, str):
                    safe_args.append(self._make_message_safe(arg))
                else:
                    safe_args.append(arg)
            
            # Get the logging method
            log_method = getattr(logger, level.lower())
            log_method(safe_message, *safe_args, **kwargs)
            
        except Exception as e:
            # Fallback to basic logging
            fallback_message = f"[LOGGING ERROR] {str(message).encode('ascii', 'replace').decode('ascii')}"
            logger.error(fallback_message)
    
    def _make_message_safe(self, message: str) -> str:
        """Replace problematic Unicode characters with safe alternatives"""
        if not isinstance(message, str):
            return str(message)
        
        # Replace common emoji and Unicode characters with text equivalents
        replacements = {
            '🎮': '[GAME]',
            '🚀': '[ROCKET]',
            '✅': '[OK]',
            '❌': '[ERROR]',
            '⚠️': '[WARNING]',
            '📊': '[CHART]',
            '📨': '[MESSAGE]',
            '🔒': '[LOCK]',
            '🔗': '[LINK]',
            '💬': '[CHAT]',
            '🐛': '[BUG]',
            'ℹ️': '[INFO]',
            '🚨': '[ALERT]',
            '📝': '[NOTE]',
            '📄': '[FILE]',
            '⏰': '[TIME]',
            '🛠️': '[TOOLS]',
            '📋': '[LIST]',
            '→': '->',
            '←': '<-',
            '↑': '^',
            '↓': 'v'
        }
        
        safe_message = message
        for unicode_char, replacement in replacements.items():
            safe_message = safe_message.replace(unicode_char, replacement)
        
        # Remove any remaining problematic characters
        try:
            safe_message.encode('ascii')
            return safe_message
        except UnicodeEncodeError:
            return safe_message.encode('ascii', 'replace').decode('ascii')

# Global logger instance
_crewai_logger = None

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance with proper configuration"""
    global _crewai_logger
    
    if _crewai_logger is None:
        _crewai_logger = CrewAILogger()
    
    if name is None:
        name = __name__
    
    return _crewai_logger.get_logger(name)

def log_safe(logger: logging.Logger, level: str, message: str, *args, **kwargs):
    """Log a message with safe Unicode handling"""
    global _crewai_logger
    
    if _crewai_logger is None:
        _crewai_logger = CrewAILogger()
    
    _crewai_logger.log_safe(logger, level, message, *args, **kwargs)

def setup_logging():
    """Initialize the logging system"""
    global _crewai_logger
    
    if _crewai_logger is None:
        _crewai_logger = CrewAILogger()
    
    return True

# Initialize logging when module is imported
setup_logging()
