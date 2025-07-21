"""
Publish Helper - Main GUI Entry Point

Copyright (C) 2023 BJD
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Project repository: https://github.com/bjdbjd/publish-helper
Contributors: bjdbjd, Pixel-LH, EasonWong0603, sertion1126, TommyMerlin
"""

import sys
from pathlib import Path

# Add project root and src directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from config.settings import config
from utils.logger import get_logger
from utils.exceptions import PublishHelperError


def main():
    """Main entry point for GUI application."""
    logger = get_logger(__name__)

    try:
        logger.info("Starting Publish Helper GUI...")
        logger.info(f"Version: {config.GUI_VERSION}")
        logger.info(f"Configuration loaded from: {config.STATIC_DIR}")

        # Import GUI module only when needed to avoid import issues
        from gui.startgui import start_gui

        # Start the GUI application
        start_gui()

    except PublishHelperError as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Publish Helper GUI stopped")


if __name__ == "__main__":
    main()
