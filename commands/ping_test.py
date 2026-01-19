"""Network ping test command implementation."""

from __future__ import annotations

import logging
import platform
import subprocess
import time
from typing import Optional

import click

from commands.exceptions import NetworkError, UserInputError

logger = logging.getLogger(__name__)


def ping_test(host: str, count: int = 4, timeout: int = 2, verbose: bool = False) -> None:
    """Test network connectivity to a host.
    
    Args:
        host: Hostname or IP address to ping
        count: Number of pings to send
        timeout: Timeout in seconds
        verbose: Show detailed output
        
    Raises:
        UserInputError: If host is invalid or empty
        NetworkError: If ping command fails or is unavailable
    """
    if not host or not host.strip():
        raise UserInputError("Host cannot be empty")
    
    host = host.strip()
    logger.info(f"Ping test requested for host: {host} (count={count}, timeout={timeout})")
    
    click.echo(f"\n🌐 Network Connectivity Test: {click.style(host, fg='cyan', bold=True)}")
    click.echo("─" * 60)
    
    # Check if ping command is available
    try:
        # Try to determine ping command based on OS
        system = platform.system().lower()
        
        if system == 'windows':
            ping_cmd = ['ping', '-n', str(count), '-w', str(timeout * 1000), host]
        else:
            ping_cmd = ['ping', '-c', str(count), '-W', str(timeout), host]
        
        if verbose:
            click.echo(f"Running: {' '.join(ping_cmd)}")
            click.echo()
        
        logger.debug(f"Executing ping command: {' '.join(ping_cmd)}")
        
        # Execute ping
        start_time = time.time()
        result = subprocess.run(
            ping_cmd,
            capture_output=True,
            text=True,
            timeout=timeout * count + 5
        )
        elapsed = time.time() - start_time
        
        logger.debug(f"Ping completed with return code {result.returncode} in {elapsed:.2f}s")
        
        # Parse results
        if result.returncode == 0:
            click.echo(click.style("✅ Host is reachable!", fg='green', bold=True))
            
            # Try to extract some stats from output
            output_lines = result.stdout.split('\n')
            stats_line = None
            for line in output_lines:
                if 'packets transmitted' in line.lower() or 'packets:' in line.lower():
                    stats_line = line.strip()
                    break
            
            if stats_line:
                click.echo(f"   {stats_line}")
            
            if verbose:
                click.echo("\nFull output:")
                click.echo(result.stdout)
        else:
            error_msg = f"Host {host} is unreachable (return code: {result.returncode})"
            logger.warning(error_msg)
            click.echo(click.style("❌ Host is unreachable!", fg='red', bold=True))
            click.echo(f"   Return code: {result.returncode}")
            
            if verbose:
                click.echo("\nError output:")
                click.echo(result.stderr)
        
        click.echo(f"\n⏱️  Test completed in {elapsed:.2f} seconds")
        
    except subprocess.TimeoutExpired as e:
        error_msg = f"Ping test timed out for {host} after {timeout} seconds"
        logger.error(error_msg)
        raise NetworkError(error_msg) from e
    except FileNotFoundError as e:
        error_msg = "ping command not found. This tool requires the 'ping' command to be available."
        logger.error(error_msg)
        raise NetworkError(
            f"{error_msg}\n"
            "On Windows, it should be built-in.\n"
            "On Linux/Mac, install: sudo apt-get install iputils-ping (Linux)"
        ) from e
    except Exception as e:
        error_msg = f"Unexpected error during ping test: {str(e)}"
        logger.exception(error_msg)
        raise NetworkError(error_msg) from e
    
    click.echo("─" * 60 + "\n")
