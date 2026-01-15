# Quick Setup Script for Windows PowerShell

Write-Host "YouTuber - Quick Setup Script" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Check Python version number
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $majorVersion = [int]$Matches[1]
    $minorVersion = [int]$Matches[2]
    if (($majorVersion -lt 3) -or (($majorVersion -eq 3) -and ($minorVersion -lt 8))) {
        Write-Host "ERROR: Python 3.8 or higher is required" -ForegroundColor Red
        exit 1
    }
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "pip upgraded" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "Dependencies installed" -ForegroundColor Green

# Install package in development mode
Write-Host ""
Write-Host "Installing YouTuber package..." -ForegroundColor Yellow
pip install -e .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install YouTuber package" -ForegroundColor Red
    exit 1
}
Write-Host "YouTuber package installed" -ForegroundColor Green

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
$ytVersion = youtuber --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: YouTuber command not found" -ForegroundColor Red
    exit 1
}
Write-Host "YouTuber is ready: $ytVersion" -ForegroundColor Green

# Check for FFmpeg
Write-Host ""
Write-Host "Checking for FFmpeg..." -ForegroundColor Yellow
$ffmpegCheck = ffmpeg -version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: FFmpeg not found" -ForegroundColor Yellow
    Write-Host "FFmpeg is optional but recommended for format conversion" -ForegroundColor Yellow
    Write-Host "Install with: winget install FFmpeg" -ForegroundColor Yellow
} else {
    Write-Host "FFmpeg is installed" -ForegroundColor Green
}

# Show application paths
Write-Host ""
Write-Host "Application paths:" -ForegroundColor Cyan
youtuber paths

Write-Host ""
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick start:" -ForegroundColor Cyan
Write-Host "  youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8" -ForegroundColor White
Write-Host ""
Write-Host "For more examples, see EXAMPLES.md" -ForegroundColor Cyan
Write-Host "For detailed documentation, see README.md" -ForegroundColor Cyan
Write-Host ""
