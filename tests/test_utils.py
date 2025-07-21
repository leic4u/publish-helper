"""Test utility modules."""

import pytest
from pathlib import Path
from src.utils.file_utils import (
    ensure_directory,
    safe_filename,
    get_file_hash,
    get_file_size_human,
)
from src.utils.logger import setup_logger


class TestFileUtils:
    """Test file utility functions."""

    def test_ensure_directory(self, tmp_path):
        """Test directory creation."""
        test_dir = tmp_path / "test" / "nested" / "directory"
        result = ensure_directory(test_dir)
        assert result.exists()
        assert result.is_dir()

    def test_safe_filename(self):
        """Test filename sanitization."""
        unsafe_name = 'file<>:"/\\|?*name.txt'
        safe_name = safe_filename(unsafe_name)
        assert "<" not in safe_name
        assert ">" not in safe_name
        assert ":" not in safe_name
        assert '"' not in safe_name
        assert "/" not in safe_name
        assert "\\" not in safe_name
        assert "|" not in safe_name
        assert "?" not in safe_name
        assert "*" not in safe_name
        assert safe_name.endswith(".txt")

    def test_safe_filename_length_limit(self):
        """Test filename length limiting."""
        long_name = "a" * 300 + ".txt"
        safe_name = safe_filename(long_name, max_length=50)
        assert len(safe_name) <= 50
        assert safe_name.endswith(".txt")

    def test_get_file_hash(self, tmp_path):
        """Test file hash calculation."""
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)

        hash_value = get_file_hash(test_file, "md5")
        assert len(hash_value) == 32  # MD5 hash length
        assert isinstance(hash_value, str)

    def test_get_file_hash_nonexistent(self, tmp_path):
        """Test file hash with nonexistent file."""
        nonexistent = tmp_path / "nonexistent.txt"
        with pytest.raises(FileNotFoundError):
            get_file_hash(nonexistent)

    def test_get_file_size_human(self):
        """Test human readable file size conversion."""
        assert get_file_size_human(0) == "0 B"
        assert get_file_size_human(1024) == "1.0 KB"
        assert get_file_size_human(1024 * 1024) == "1.0 MB"
        assert get_file_size_human(1024 * 1024 * 1024) == "1.0 GB"


class TestLogger:
    """Test logging utilities."""

    def test_setup_logger(self, tmp_path):
        """Test logger setup."""
        log_file = tmp_path / "test.log"
        logger = setup_logger("test_logger", "DEBUG", log_file, True)

        logger.info("Test message")

        assert log_file.exists()
        log_content = log_file.read_text()
        assert "Test message" in log_content

    def test_logger_without_file(self):
        """Test logger setup without file output."""
        logger = setup_logger("test_logger_no_file", "INFO", None, True)

        # Should not raise an exception
        logger.info("Test message without file")

        assert logger.level == 20  # INFO level
