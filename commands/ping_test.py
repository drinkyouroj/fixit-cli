"""Network ping test command implementation."""

import click
import subprocess
import time


def ping_test(host, count=4, timeout=2, verbose=False):
    """
    Test network connectivity to a host.
    
    Args:
        host: Hostname or IP address to ping
        count: Number of pings to send
        timeout: Timeout in seconds
        verbose: Show detailed output
    """
    click.echo(f"\n🌐 Network Connectivity Test: {click.style(host, fg='cyan', bold=True)}")
    click.echo("─" * 60)
    
    # Check if ping command is available
    try:
        # Try to determine ping command based on OS
        import platform
        system = platform.system().lower()
        
        if system == 'windows':
            ping_cmd = ['ping', '-n', str(count), '-w', str(timeout * 1000), host]
        else:
            ping_cmd = ['ping', '-c', str(count), '-W', str(timeout), host]
        
        if verbose:
            click.echo(f"Running: {' '.join(ping_cmd)}")
            click.echo()
        
        # Execute ping
        start_time = time.time()
        result = subprocess.run(
            ping_cmd,
            capture_output=True,
            text=True,
            timeout=timeout * count + 5
        )
        elapsed = time.time() - start_time
        
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
            click.echo(click.style("❌ Host is unreachable!", fg='red', bold=True))
            click.echo(f"   Return code: {result.returncode}")
            
            if verbose:
                click.echo("\nError output:")
                click.echo(result.stderr)
        
        click.echo(f"\n⏱️  Test completed in {elapsed:.2f} seconds")
        
    except subprocess.TimeoutExpired:
        click.echo(click.style("⏱️  Ping test timed out!", fg='yellow', bold=True))
        click.echo(f"   Host: {host}")
        click.echo(f"   Timeout: {timeout} seconds")
    except FileNotFoundError:
        click.echo(click.style("❌ Error: ping command not found!", fg='red', bold=True))
        click.echo("   This tool requires the 'ping' command to be available.")
        click.echo("   On Windows, it should be built-in.")
        click.echo("   On Linux/Mac, install: sudo apt-get install iputils-ping (Linux)")
    except Exception as e:
        click.echo(click.style(f"❌ Error: {str(e)}", fg='red', bold=True))
    
    click.echo("─" * 60 + "\n")
