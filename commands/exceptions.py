"""Shared exception types for Fix-It CLI commands.

These exceptions are raised by command implementations and handled by the CLI
entrypoint to present consistent, user-friendly error messages.
"""

from __future__ import annotations


class FixitError(Exception):
    """Base exception for Fix-It CLI."""


class UserInputError(FixitError):
    """Raised when user-provided input is invalid."""


class LogFileError(FixitError):
    """Raised when log file operations fail."""


class NetworkError(FixitError):
    """Raised when network operations fail."""

