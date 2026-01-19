"""Log dump command implementation."""

from __future__ import annotations

import gzip
import logging
from pathlib import Path
from typing import Optional

import click

from commands.exceptions import LogFileError, UserInputError

logger = logging.getLogger(__name__)


def is_gzipped(filepath: Path) -> bool:
    """Check if a file is gzipped.
    
    Args:
        filepath: Path to the file to check
        
    Returns:
        True if the file appears to be gzipped, False otherwise
    """
    try:
        with open(filepath, 'rb') as f:
            return f.read(2) == b'\x1f\x8b'
    except Exception:
        return False


def log_dump(
    log_path: str,
    lines: int = 50,
    tail: bool = False,
    grep: Optional[str] = None,
    output: Optional[str] = None,
) -> None:
    """Dump log file contents with filtering options.
    
    Args:
        log_path: Path to the log file
        lines: Number of lines to show
        tail: Show tail instead of head
        grep: Filter pattern to search for
        output: Optional output file path
        
    Raises:
        UserInputError: If log_path is invalid or empty
        LogFileError: If file operations fail
    """
    if not log_path or not log_path.strip():
        raise UserInputError("Log path cannot be empty")
    
    log_file = Path(log_path.strip())
    logger.info(f"Log dump requested for: {log_file} (lines={lines}, tail={tail}, grep={grep})")
    
    click.echo(f"\n📋 Log Dump: {click.style(str(log_file), fg='cyan', bold=True)}")
    click.echo("─" * 60)
    
    # Check if file exists
    if not log_file.exists():
        error_msg = f"File not found: {log_file}"
        logger.error(error_msg)
        raise LogFileError(error_msg)
    
    # Check if file is readable
    if not log_file.is_file():
        error_msg = f"Not a regular file: {log_file}"
        logger.error(error_msg)
        raise LogFileError(error_msg)
    
    try:
        # Handle gzipped files
        if is_gzipped(log_file):
            logger.debug(f"Detected gzipped file: {log_file}")
            click.echo("📦 Detected gzipped file, decompressing...")
            file_handle = gzip.open(log_file, 'rt', encoding='utf-8', errors='ignore')
        else:
            file_handle = open(log_file, 'r', encoding='utf-8', errors='ignore')
        
        with file_handle as f:
            all_lines = f.readlines()
        
        logger.debug(f"Read {len(all_lines)} lines from {log_file}")
        
        # Apply grep filter if specified
        if grep:
            filtered_lines = [line for line in all_lines if grep.lower() in line.lower()]
            click.echo(f"🔍 Filtering for pattern: {click.style(grep, fg='yellow')}")
            click.echo(f"   Found {len(filtered_lines)} matching lines out of {len(all_lines)} total")
            all_lines = filtered_lines
            logger.debug(f"Filtered to {len(filtered_lines)} matching lines")
        
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
            try:
                output_path.write_text(output_content, encoding='utf-8')
                logger.info(f"Output saved to: {output_path}")
                click.echo(click.style(f"✅ Output saved to: {output_path}", fg='green', bold=True))
            except Exception as e:
                error_msg = f"Failed to write output file {output_path}: {str(e)}"
                logger.error(error_msg)
                raise LogFileError(error_msg) from e
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
        
    except PermissionError as e:
        error_msg = f"Permission denied reading {log_file}"
        logger.error(error_msg)
        raise LogFileError(error_msg) from e
    except Exception as e:
        if isinstance(e, LogFileError):
            raise
        error_msg = f"Error reading file: {str(e)}"
        logger.exception(error_msg)
        raise LogFileError(error_msg) from e
    
    click.echo("─" * 60 + "\n")
