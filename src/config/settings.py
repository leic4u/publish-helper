"""Application settings and configuration management."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Application configuration class."""

    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load environment variables from .env file
        load_dotenv()

        # Base paths
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.SRC_DIR = self.BASE_DIR / "src"
        self.STATIC_DIR = self.BASE_DIR / "static"
        self.TEMP_DIR = self.BASE_DIR / "temp"
        self.MEDIA_DIR = self.BASE_DIR / "media"
        self.LOGS_DIR = self.BASE_DIR / "logs"

        # Ensure directories exist
        self._create_directories()

        # API Configuration
        self.API_HOST = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT = int(os.getenv("API_PORT", "15372"))
        self.API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"

        # GUI Configuration
        self.GUI_TITLE = os.getenv("GUI_TITLE", "Publish Helper")
        self.GUI_VERSION = os.getenv("GUI_VERSION", "1.4.5")

        # PT-Gen Configuration
        self.PTGEN_API_URL = os.getenv("PTGEN_API_URL", "")
        self.PTGEN_API_KEY = os.getenv("PTGEN_API_KEY", "")

        # Image Hosting Configuration
        self.IMAGE_HOST_TYPE = os.getenv("IMAGE_HOST_TYPE", "freeimage")
        self.IMAGE_HOST_API_URL = os.getenv("IMAGE_HOST_API_URL", "")
        self.IMAGE_HOST_API_KEY = os.getenv("IMAGE_HOST_API_KEY", "")

        # Media Info Configuration
        self.MEDIAINFO_PATH = os.getenv("MEDIAINFO_PATH", "")

        # Logging Configuration
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = self.LOGS_DIR / os.getenv("LOG_FILE", "app.log")

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.STATIC_DIR,
            self.TEMP_DIR,
            self.TEMP_DIR / "pic",
            self.TEMP_DIR / "torrent",
            self.MEDIA_DIR,
            self.LOGS_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def get_temp_pic_dir(self) -> Path:
        """Get temporary picture directory."""
        return self.TEMP_DIR / "pic"

    def get_temp_torrent_dir(self) -> Path:
        """Get temporary torrent directory."""
        return self.TEMP_DIR / "torrent"

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return os.getenv("ENVIRONMENT", "production").lower() == "development"


# Global configuration instance
config = Config()


class ImageHostConfig:
    """Configuration for different image hosting services."""

    SUPPORTED_HOSTS = {
        "freeimage": {
            "name": "FreeImage",
            "api_url": "https://freeimage.host/api/1/upload",
            "requires_key": False,
        },
        "imgbb": {
            "name": "ImgBB",
            "api_url": "https://api.imgbb.com/1/upload",
            "requires_key": True,
        },
        "imagehub": {
            "name": "ImageHub",
            "api_url": "https://www.imagehub.cc/api/1/upload",
            "requires_key": False,
        },
        "pixhost": {
            "name": "PixHost",
            "api_url": "https://api.pixhost.to/images",
            "requires_key": False,
        },
        "bohe": {
            "name": "薄荷图床",
            "api_url": "",  # To be configured by user
            "requires_key": True,
        },
        "lsky-pro": {
            "name": "兰空图床",
            "api_url": "",  # To be configured by user
            "requires_key": True,
        },
        "chevereto": {
            "name": "Chevereto",
            "api_url": "",  # To be configured by user
            "requires_key": True,
        },
    }

    @classmethod
    def get_host_config(cls, host_type: str) -> Optional[dict]:
        """Get configuration for a specific image host."""
        return cls.SUPPORTED_HOSTS.get(host_type)

    @classmethod
    def get_supported_hosts(cls) -> list[str]:
        """Get list of supported image host types."""
        return list(cls.SUPPORTED_HOSTS.keys())
