"""Log dump command implementation."""

import click
import gzip
from pathlib import Path
from datetime import datetime


def is_gzipped(filepath):
    """Check if a file is gzipped."""
    try:
        with open(filepath, 'rb') as f:
            return f.read(2) == b'\x1f\x8b'
    except:
        return False


def log_dump(log_path, lines=50, tail=False, grep=None, output=None):
    """
    Dump log file contents with filtering options.
    
    Args:
        log_path: Path to the log file
        lines: Number of lines to show
        tail: Show tail instead of head
        grep: Filter pattern to search for
        output: Optional output file path
    """
    log_file = Path(log_path)
    
    click.echo(f"\n📋 Log Dump: {click.style(str(log_file), fg='cyan', bold=True)}")
    click.echo("─" * 60)
    
    # Check if file exists
    if not log_file.exists():
        click.echo(click.style(f"❌ Error: File not found: {log_file}", fg='red', bold=True))
        return
    
    # Check if file is readable
    if not log_file.is_file():
        click.echo(click.style(f"❌ Error: Not a regular file: {log_file}", fg='red', bold=True))
        return
    
    try:
        # Handle gzipped files
        if is_gzipped(log_file):
            click.echo("📦 Detected gzipped file, decompressing...")
            file_handle = gzip.open(log_file, 'rt', encoding='utf-8', errors='ignore')
        else:
            file_handle = open(log_file, 'r', encoding='utf-8', errors='ignore')
        
        with file_handle as f:
            all_lines = f.readlines()
        
        # Apply grep filter if specified
        if grep:
            filtered_lines = [line for line in all_lines if grep.lower() in line.lower()]
            click.echo(f"🔍 Filtering for pattern: {click.style(grep, fg='yellow')}")
            click.echo(f"   Found {len(filtered_lines)} matching lines out of {len(all_lines)} total")
            all_lines = filtered_lines
        
        # Select lines (head or tail)
        if tail:
            selected_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            position = "tail"
        else:
            selected_lines = all_lines[:lines] if len(all_lines) > lines else all_lines
            position = "head"
        
        # Display info
        total_lines = len(all_lines)
        shown_lines = len(selected_lines)
        click.echo(f"📊 Showing {shown_lines} lines from {position} (total: {total_lines} lines)")
        click.echo()
        
        # Output to file or console
        output_content = ''.join(selected_lines)
        
        if output:
            output_path = Path(output)
            output_path.write_text(output_content, encoding='utf-8')
            click.echo(click.style(f"✅ Output saved to: {output_path}", fg='green', bold=True))
        else:
            # Display with line numbers
            for i, line in enumerate(selected_lines, start=1):
                # Highlight grep matches
                if grep and grep.lower() in line.lower():
                    # Simple highlighting - replace matched text with styled version
                    highlighted = line.replace(
                        grep,
                        click.style(grep, fg='yellow', bold=True)
                    )
                    click.echo(f"{i:4d} │ {highlighted.rstrip()}")
                else:
                    click.echo(f"{i:4d} │ {line.rstrip()}")
        
        click.echo()
        click.echo(f"💡 Tip: Use --tail to see the end, --grep to filter, --output to save")
        
    except PermissionError:
        click.echo(click.style(f"❌ Error: Permission denied reading {log_file}", fg='red', bold=True))
    except Exception as e:
        click.echo(click.style(f"❌ Error reading file: {str(e)}", fg='red', bold=True))
    
    click.echo("─" * 60 + "\n")
