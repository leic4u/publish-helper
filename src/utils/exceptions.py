"""Exception classes for the application."""


class PublishHelperError(Exception):
    """Base exception class for Publish Helper."""

    pass


class ConfigurationError(PublishHelperError):
    """Exception raised for configuration errors."""

    pass


class MediaInfoError(PublishHelperError):
    """Exception raised for media info processing errors."""

    pass


class ScreenshotError(PublishHelperError):
    """Exception raised for screenshot processing errors."""

    pass


class ImageUploadError(PublishHelperError):
    """Exception raised for image upload errors."""

    pass


class TorrentError(PublishHelperError):
    """Exception raised for torrent creation errors."""

    pass


class PTGenError(PublishHelperError):
    """Exception raised for PT-Gen API errors."""

    pass


class RenameError(PublishHelperError):
    """Exception raised for file renaming errors."""

    pass


class ValidationError(PublishHelperError):
    """Exception raised for validation errors."""

    pass
