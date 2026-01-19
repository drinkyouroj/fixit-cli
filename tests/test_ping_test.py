"""Tests for ping_test command."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from commands.exceptions import NetworkError, UserInputError
from commands.ping_test import ping_test
from fixit import cli


class TestPingTest:
    """Test ping_test function."""

    def test_ping_test_empty_host(self):
        """Test that empty host raises UserInputError."""
        with pytest.raises(UserInputError, match="Host cannot be empty"):
            ping_test("")

    def test_ping_test_whitespace_host(self):
        """Test that whitespace-only host raises UserInputError."""
        with pytest.raises(UserInputError, match="Host cannot be empty"):
            ping_test("   ")

    @patch("commands.ping_test.subprocess.run")
    def test_ping_test_success(self, mock_subprocess):
        """Test successful ping."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "4 packets transmitted, 4 received, 0% packet loss"
        mock_subprocess.return_value = mock_result

        # Should not raise
        ping_test("example.com", count=4, timeout=2)

    @patch("commands.ping_test.subprocess.run")
    def test_ping_test_unreachable(self, mock_subprocess):
        """Test unreachable host."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Host unreachable"
        mock_subprocess.return_value = mock_result

        # Should not raise, just log warning
        ping_test("unreachable.example.com", count=1, timeout=1)

    @patch("commands.ping_test.subprocess.run")
    def test_ping_test_timeout(self, mock_subprocess):
        """Test ping timeout."""
        mock_subprocess.side_effect = subprocess.TimeoutExpired("ping", 5)

        with pytest.raises(NetworkError, match="timed out"):
            ping_test("slow.example.com", count=1, timeout=1)

    @patch("commands.ping_test.subprocess.run")
    def test_ping_test_command_not_found(self, mock_subprocess):
        """Test when ping command is not found."""
        mock_subprocess.side_effect = FileNotFoundError("ping command not found")

        with pytest.raises(NetworkError, match="ping command not found"):
            ping_test("example.com")


class TestPingTestCLI:
    """Test ping-test CLI command."""

    def test_ping_test_command_help(self):
        """Test that help text is displayed."""
        runner = CliRunner()
        result = runner.invoke(cli, ["ping-test", "--help"])
        assert result.exit_code == 0
        assert "Test network connectivity" in result.output

    @patch("commands.ping_test.subprocess.run")
    def test_ping_test_command_basic(self, mock_subprocess):
        """Test basic ping test command."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "4 packets transmitted, 4 received"
        mock_subprocess.return_value = mock_result

        runner = CliRunner()
        result = runner.invoke(cli, ["ping-test", "example.com"])
        assert result.exit_code == 0
        assert "Network Connectivity Test" in result.output

    @patch("commands.ping_test.subprocess.run")
    def test_ping_test_command_with_options(self, mock_subprocess):
        """Test ping test command with options."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "10 packets transmitted"
        mock_subprocess.return_value = mock_result

        runner = CliRunner()
        result = runner.invoke(
            cli, ["ping-test", "example.com", "--count", "10", "--timeout", "5", "--verbose"]
        )
        assert result.exit_code == 0

    def test_ping_test_command_empty_host(self):
        """Test ping test command with empty host."""
        runner = CliRunner()
        result = runner.invoke(cli, ["ping-test", ""])
        assert result.exit_code == 1
        assert "Host cannot be empty" in result.output
