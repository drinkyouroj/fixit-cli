#!/usr/bin/env python3
"""
Fix-It CLI: IT Support Toolkit
A command-line tool that mimics real-life IT support tasks with a touch of humor.
"""

from __future__ import annotations

import click
import logging
import traceback
from datetime import datetime
from typing import Optional

# Import command modules
from commands.reset_user import reset_user
from commands.ping_test import ping_test
from commands.log_dump import log_dump
from commands.exceptions import FixitError


__version__ = "1.0.0"


def _configure_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _handle_error(exc: Exception, debug: bool) -> None:
    if isinstance(exc, FixitError):
        click.echo(click.style(f"❌ {exc}", fg="red", bold=True))
        return

    click.echo(click.style("❌ Unexpected error occurred.", fg="red", bold=True))
    if debug:
        click.echo(click.style("Debug traceback:", fg="yellow", bold=True))
        click.echo("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))


@click.group()
@click.version_option(version=__version__, prog_name="fixit")
@click.option(
    "--log-level",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"], case_sensitive=False),
    default="WARNING",
    show_default=True,
    help="Logging verbosity for diagnostics.",
)
@click.pass_context
def cli(ctx: click.Context, log_level: str) -> None:
    """
    🔧 Fix-It CLI: Your friendly neighborhood IT support toolkit.
    
    Because sometimes you need to fix things, and sometimes you need to pretend you're fixing things.
    
    Use 'fixit <command> --help' to see help for any command.
    """
    ctx.ensure_object(dict)
    ctx.obj['start_time'] = datetime.now()
    ctx.obj["log_level"] = log_level.upper()
    _configure_logging(ctx.obj["log_level"])


@cli.command()
@click.argument('username')
@click.option('--force', '-f', is_flag=True, help='Force reset without confirmation (use with caution!)')
@click.option('--email', '-e', help='Send reset notification to this email')
@click.pass_context
def reset_user_cmd(ctx: click.Context, username: str, force: bool, email: Optional[str]) -> None:
    """Reset a user's password (simulated, of course)."""
    try:
        reset_user(username, force, email)
    except Exception as exc:  # noqa: BLE001 - CLI boundary: render friendly message
        _handle_error(exc, debug=ctx.obj.get("log_level") == "DEBUG")
        raise SystemExit(1) from exc


@cli.command()
@click.argument('host')
@click.option('--count', '-c', default=4, help='Number of pings to send')
@click.option('--timeout', '-t', default=2, help='Timeout in seconds')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.pass_context
def ping_test_cmd(
    ctx: click.Context, host: str, count: int, timeout: int, verbose: bool
) -> None:
    """Test network connectivity to a host."""
    try:
        ping_test(host, count, timeout, verbose)
    except Exception as exc:  # noqa: BLE001 - CLI boundary: render friendly message
        _handle_error(exc, debug=ctx.obj.get("log_level") == "DEBUG")
        raise SystemExit(1) from exc


@cli.command()
@click.argument('log_path', type=click.Path())
@click.option('--lines', '-n', default=50, help='Number of lines to dump (default: 50)')
@click.option('--tail', '-t', is_flag=True, help='Show tail instead of head')
@click.option('--grep', '-g', help='Filter lines containing this pattern')
@click.option('--output', '-o', type=click.Path(), help='Save output to file')
@click.pass_context
def log_dump_cmd(
    ctx: click.Context,
    log_path: str,
    lines: int,
    tail: bool,
    grep: Optional[str],
    output: Optional[str],
) -> None:
    """Dump log file contents with various filtering options."""
    try:
        log_dump(log_path, lines, tail, grep, output)
    except Exception as exc:  # noqa: BLE001 - CLI boundary: render friendly message
        _handle_error(exc, debug=ctx.obj.get("log_level") == "DEBUG")
        raise SystemExit(1) from exc


if __name__ == '__main__':
    cli()
