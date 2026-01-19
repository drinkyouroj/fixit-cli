"""Tests for reset_user command."""

import pytest
from click.testing import CliRunner

from commands.exceptions import UserInputError
from commands.reset_user import generate_password, reset_user
from fixit import cli


class TestGeneratePassword:
    """Test password generation."""

    def test_generate_password_default_length(self):
        """Test password generation with default length."""
        password = generate_password()
        assert len(password) == 12
        assert any(c.isalpha() for c in password)
        assert any(c.isdigit() for c in password)

    def test_generate_password_custom_length(self):
        """Test password generation with custom length."""
        password = generate_password(16)
        assert len(password) == 16

    def test_generate_password_uniqueness(self):
        """Test that generated passwords are unique."""
        passwords = {generate_password() for _ in range(100)}
        assert len(passwords) > 90  # Very high probability of uniqueness


class TestResetUser:
    """Test reset_user function."""

    def test_reset_user_empty_username(self):
        """Test that empty username raises UserInputError."""
        with pytest.raises(UserInputError, match="Username cannot be empty"):
            reset_user("")

    def test_reset_user_whitespace_username(self):
        """Test that whitespace-only username raises UserInputError."""
        with pytest.raises(UserInputError, match="Username cannot be empty"):
            reset_user("   ")


class TestResetUserCLI:
    """Test reset-user CLI command."""

    def test_reset_user_command_help(self):
        """Test that help text is displayed."""
        runner = CliRunner()
        result = runner.invoke(cli, ["reset-user", "--help"])
        assert result.exit_code == 0
        assert "Reset a user's password" in result.output

    def test_reset_user_command_basic(self):
        """Test basic reset user command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["reset-user", "testuser"], input="y\n")
        assert result.exit_code == 0
        assert "Password Reset Request" in result.output
        assert "testuser" in result.output

    def test_reset_user_command_force(self):
        """Test reset user command with --force flag."""
        runner = CliRunner()
        result = runner.invoke(cli, ["reset-user", "testuser", "--force"])
        assert result.exit_code == 0
        assert "Password Reset Successful" in result.output

    def test_reset_user_command_with_email(self):
        """Test reset user command with email option."""
        runner = CliRunner()
        result = runner.invoke(
            cli, ["reset-user", "testuser", "--force", "--email", "test@example.com"]
        )
        assert result.exit_code == 0
        assert "test@example.com" in result.output

    def test_reset_user_command_cancelled(self):
        """Test reset user command when cancelled."""
        runner = CliRunner()
        result = runner.invoke(cli, ["reset-user", "testuser"], input="n\n")
        assert result.exit_code == 0
        assert "cancelled" in result.output.lower()

    def test_reset_user_command_empty_username(self):
        """Test reset user command with empty username."""
        runner = CliRunner()
        result = runner.invoke(cli, ["reset-user", ""])
        assert result.exit_code == 1
        assert "Username cannot be empty" in result.output
