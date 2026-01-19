"""Tests for log_dump command."""

import gzip
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from commands.exceptions import LogFileError, UserInputError
from commands.log_dump import is_gzipped, log_dump
from fixit import cli


class TestIsGzipped:
    """Test is_gzipped function."""

    def test_is_gzipped_true(self):
        """Test detection of gzipped file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gz") as f:
            with gzip.open(f.name, "wt") as gz:
                gz.write("test content")
            path = Path(f.name)
            assert is_gzipped(path) is True
            path.unlink()

    def test_is_gzipped_false(self):
        """Test detection of non-gzipped file."""
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
            f.write("test content")
            path = Path(f.name)
            assert is_gzipped(path) is False
            path.unlink()


class TestLogDump:
    """Test log_dump function."""

    def test_log_dump_empty_path(self):
        """Test that empty path raises UserInputError."""
        with pytest.raises(UserInputError, match="Log path cannot be empty"):
            log_dump("")

    def test_log_dump_whitespace_path(self):
        """Test that whitespace-only path raises UserInputError."""
        with pytest.raises(UserInputError, match="Log path cannot be empty"):
            log_dump("   ")

    def test_log_dump_file_not_found(self):
        """Test that missing file raises LogFileError."""
        with pytest.raises(LogFileError, match="File not found"):
            log_dump("/nonexistent/path/to/file.log")

    def test_log_dump_basic(self):
        """Test basic log dump functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
            log_path = f.name

        try:
            # Should not raise
            log_dump(log_path, lines=3)
        finally:
            Path(log_path).unlink()

    def test_log_dump_tail(self):
        """Test log dump with tail option."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
            log_path = f.name

        try:
            # Should not raise
            log_dump(log_path, lines=2, tail=True)
        finally:
            Path(log_path).unlink()

    def test_log_dump_grep(self):
        """Test log dump with grep filter."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("INFO: Message 1\nERROR: Message 2\nINFO: Message 3\n")
            log_path = f.name

        try:
            # Should not raise
            log_dump(log_path, grep="ERROR")
        finally:
            Path(log_path).unlink()

    def test_log_dump_gzipped(self):
        """Test log dump with gzipped file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".gz") as f:
            with gzip.open(f.name, "wt") as gz:
                gz.write("Line 1\nLine 2\nLine 3\n")
            log_path = f.name

        try:
            # Should not raise
            log_dump(log_path)
        finally:
            Path(log_path).unlink()

    def test_log_dump_output_file(self):
        """Test log dump with output file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("Line 1\nLine 2\nLine 3\n")
            log_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".out") as f:
            output_path = f.name

        try:
            log_dump(log_path, output=output_path)
            assert Path(output_path).exists()
            assert Path(output_path).read_text() == "Line 1\nLine 2\nLine 3\n"
        finally:
            Path(log_path).unlink()
            if Path(output_path).exists():
                Path(output_path).unlink()


class TestLogDumpCLI:
    """Test log-dump CLI command."""

    def test_log_dump_command_help(self):
        """Test that help text is displayed."""
        runner = CliRunner()
        result = runner.invoke(cli, ["log-dump", "--help"])
        assert result.exit_code == 0
        assert "Dump log file contents" in result.output

    def test_log_dump_command_basic(self):
        """Test basic log dump command."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("Line 1\nLine 2\nLine 3\n")
            log_path = f.name

        try:
            runner = CliRunner()
            result = runner.invoke(cli, ["log-dump", log_path])
            assert result.exit_code == 0
            assert "Log Dump" in result.output
        finally:
            Path(log_path).unlink()

    def test_log_dump_command_with_options(self):
        """Test log dump command with options."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write("INFO: Message\nERROR: Error message\nWARN: Warning\n")
            log_path = f.name

        try:
            runner = CliRunner()
            result = runner.invoke(
                cli, ["log-dump", log_path, "--lines", "10", "--tail", "--grep", "ERROR"]
            )
            assert result.exit_code == 0
            assert "ERROR" in result.output
        finally:
            Path(log_path).unlink()

    def test_log_dump_command_file_not_found(self):
        """Test log dump command with non-existent file."""
        runner = CliRunner()
        result = runner.invoke(cli, ["log-dump", "/nonexistent/file.log"])
        assert result.exit_code == 1
        assert "File not found" in result.output

    def test_log_dump_command_empty_path(self):
        """Test log dump command with empty path."""
        runner = CliRunner()
        result = runner.invoke(cli, ["log-dump", ""])
        assert result.exit_code == 1
        assert "Log path cannot be empty" in result.output
