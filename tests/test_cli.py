"""Integration tests for CLI."""

from click.testing import CliRunner

from fixit import cli


class TestCLI:
    """Test CLI entrypoint."""

    def test_cli_help(self):
        """Test that main help text is displayed."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Fix-It CLI" in result.output

    def test_cli_version(self):
        """Test version option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "fixit" in result.output
        assert "1.0.0" in result.output

    def test_cli_log_level_option(self):
        """Test log level option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--log-level", "DEBUG", "--help"])
        assert result.exit_code == 0

    def test_cli_invalid_command(self):
        """Test invalid command handling."""
        runner = CliRunner()
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.output or "Usage:" in result.output
