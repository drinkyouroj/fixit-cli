#!/usr/bin/env python3
"""Setup script for Fix-It CLI."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="fixit-cli",
    version="1.0.0",
    description="🔧 Fix-It CLI: IT Support Toolkit - A command-line tool for IT support tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/fixit-cli",
    py_modules=["fixit"],
    packages=["commands"],
    install_requires=[
        "click>=8.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "fixit=fixit:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="cli it-support sysadmin tools automation",
)
