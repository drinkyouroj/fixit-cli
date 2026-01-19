#!/usr/bin/env python3
"""
Fix-It CLI: IT Support Toolkit
A command-line tool that mimics real-life IT support tasks with a touch of humor.
"""

import click
from datetime import datetime

# Import command modules
from commands.reset_user import reset_user
from commands.ping_test import ping_test
from commands.log_dump import log_dump


@click.group()
@click.version_option(version='1.0.0', prog_name='fixit')
@click.pass_context
def cli(ctx):
    """
    🔧 Fix-It CLI: Your friendly neighborhood IT support toolkit.
    
    Because sometimes you need to fix things, and sometimes you need to pretend you're fixing things.
    
    Use 'fixit <command> --help' to see help for any command.
    """
    ctx.ensure_object(dict)
    ctx.obj['start_time'] = datetime.now()


@cli.command()
@click.argument('username')
@click.option('--force', '-f', is_flag=True, help='Force reset without confirmation (use with caution!)')
@click.option('--email', '-e', help='Send reset notification to this email')
def reset_user_cmd(username, force, email):
    """Reset a user's password (simulated, of course)."""
    reset_user(username, force, email)


@cli.command()
@click.argument('host')
@click.option('--count', '-c', default=4, help='Number of pings to send')
@click.option('--timeout', '-t', default=2, help='Timeout in seconds')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def ping_test_cmd(host, count, timeout, verbose):
    """Test network connectivity to a host."""
    ping_test(host, count, timeout, verbose)


@cli.command()
@click.argument('log_path', type=click.Path())
@click.option('--lines', '-n', default=50, help='Number of lines to dump (default: 50)')
@click.option('--tail', '-t', is_flag=True, help='Show tail instead of head')
@click.option('--grep', '-g', help='Filter lines containing this pattern')
@click.option('--output', '-o', type=click.Path(), help='Save output to file')
def log_dump_cmd(log_path, lines, tail, grep, output):
    """Dump log file contents with various filtering options."""
    log_dump(log_path, lines, tail, grep, output)


if __name__ == '__main__':
    cli()
