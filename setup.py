"""Setup script for YouTuber package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="youtuber",
    version="1.0.0",
    author="YouTuber Developer",
    description="Professional cross-platform YouTube video downloader with collection management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtuber",
    packages=find_packages(where="."),
    package_dir={},
    py_modules=[],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2024.12.0",
        "click>=8.1.0",
        "rich>=13.7.0",
        "platformdirs>=4.0.0",
        "requests>=2.31.0",
        "python-dateutil>=2.8.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "youtuber=youtuber.cli:main",
            "yt=youtuber.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
    ],
    keywords="youtube downloader cli video transcript collection",
    project_urls={
        "Homepage": "https://github.com/yourusername/youtuber",
        "Bug Reports": "https://github.com/yourusername/youtuber/issues",
        "Source": "https://github.com/yourusername/youtuber",
    },
)
