"""Test configuration module."""

import pytest
from pathlib import Path
from src.config.settings import Config
from src.core.settings_tool import SettingsManager


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary configuration directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def temp_settings_manager(temp_config_dir):
    """Create a settings manager with temporary directory."""
    settings_file = temp_config_dir / "settings.json"
    return SettingsManager(settings_file)


class TestConfig:
    """Test configuration class."""

    def test_config_initialization(self):
        """Test that config initializes properly."""
        config = Config()
        assert config.API_HOST == "0.0.0.0"
        assert config.API_PORT == 15372
        assert isinstance(config.BASE_DIR, Path)

    def test_directory_creation(self, tmp_path, monkeypatch):
        """Test that necessary directories are created."""
        # Mock the base directory
        mock_base = tmp_path / "test_app"

        with monkeypatch.context() as m:
            m.setenv("BASE_DIR", str(mock_base))
            config = Config()

        # Check that directories exist
        assert config.STATIC_DIR.exists()
        assert config.TEMP_DIR.exists()
        assert config.MEDIA_DIR.exists()
        assert config.LOGS_DIR.exists()


class TestSettingsManager:
    """Test settings manager."""

    def test_settings_manager_initialization(self, temp_settings_manager):
        """Test that settings manager initializes correctly."""
        assert temp_settings_manager.settings_file.exists()

    def test_get_setting(self, temp_settings_manager):
        """Test getting a setting value."""
        value = temp_settings_manager.get_setting("api_port", "5000")
        assert value == "15372"  # Default value

    def test_update_setting(self, temp_settings_manager):
        """Test updating a setting value."""
        temp_settings_manager.update_setting("test_key", "test_value")
        assert temp_settings_manager.get_setting("test_key") == "test_value"

    def test_environment_variable_override(self, temp_settings_manager, monkeypatch):
        """Test that environment variables override settings."""
        monkeypatch.setenv("API_PORT", "9999")
        value = temp_settings_manager.get_setting("api_port")
        assert value == "9999"

    def test_legacy_key_handling(self, temp_settings_manager):
        """Test legacy key compatibility."""
        temp_settings_manager.update_setting(
            "test_template", "Template with {category}"
        )
        value = temp_settings_manager.get_setting("test_template")
        assert "{categories}" in value
        assert "{category}" not in value
