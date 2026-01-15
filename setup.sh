#!/bin/bash
# Quick Setup Script for Linux/macOS

echo -e "\033[0;36mYouTuber - Quick Setup Script\033[0m"
echo -e "\033[0;36m=============================\033[0m"
echo ""

# Check Python version
echo -e "\033[0;33mChecking Python version...\033[0m"
if ! command -v python3 &> /dev/null; then
    echo -e "\033[0;31mERROR: Python 3 is not installed\033[0m"
    echo -e "\033[0;31mPlease install Python 3.8 or higher\033[0m"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "\033[0;32mFound: $PYTHON_VERSION\033[0m"

# Check Python version number
MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo -e "\033[0;31mERROR: Python 3.8 or higher is required\033[0m"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "\033[0;33mCreating virtual environment...\033[0m"
if [ -d "venv" ]; then
    echo -e "\033[0;32mVirtual environment already exists\033[0m"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mERROR: Failed to create virtual environment\033[0m"
        exit 1
    fi
    echo -e "\033[0;32mVirtual environment created\033[0m"
fi

# Activate virtual environment
echo ""
echo -e "\033[0;33mActivating virtual environment...\033[0m"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to activate virtual environment\033[0m"
    exit 1
fi
echo -e "\033[0;32mVirtual environment activated\033[0m"

# Upgrade pip
echo ""
echo -e "\033[0;33mUpgrading pip...\033[0m"
python -m pip install --upgrade pip
echo -e "\033[0;32mpip upgraded\033[0m"

# Install requirements
echo ""
echo -e "\033[0;33mInstalling dependencies...\033[0m"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to install dependencies\033[0m"
    exit 1
fi
echo -e "\033[0;32mDependencies installed\033[0m"

# Install package in development mode
echo ""
echo -e "\033[0;33mInstalling YouTuber package...\033[0m"
pip install -e .
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: Failed to install YouTuber package\033[0m"
    exit 1
fi
echo -e "\033[0;32mYouTuber package installed\033[0m"

# Verify installation
echo ""
echo -e "\033[0;33mVerifying installation...\033[0m"
YT_VERSION=$(youtuber --version 2>&1)
if [ $? -ne 0 ]; then
    echo -e "\033[0;31mERROR: YouTuber command not found\033[0m"
    exit 1
fi
echo -e "\033[0;32mYouTuber is ready: $YT_VERSION\033[0m"

# Check for FFmpeg
echo ""
echo -e "\033[0;33mChecking for FFmpeg...\033[0m"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "\033[0;33mWARNING: FFmpeg not found\033[0m"
    echo -e "\033[0;33mFFmpeg is optional but recommended for format conversion\033[0m"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "\033[0;33mInstall with: brew install ffmpeg\033[0m"
    else
        echo -e "\033[0;33mInstall with: sudo apt install ffmpeg\033[0m"
    fi
else
    echo -e "\033[0;32mFFmpeg is installed\033[0m"
fi

# Show application paths
echo ""
echo -e "\033[0;36mApplication paths:\033[0m"
youtuber paths

echo ""
echo -e "\033[0;36m=============================\033[0m"
echo -e "\033[0;32mSetup Complete!\033[0m"
echo -e "\033[0;36m=============================\033[0m"
echo ""
echo -e "\033[0;36mQuick start:\033[0m"
echo -e "\033[0;37m  youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8\033[0m"
echo ""
echo -e "\033[0;36mFor more examples, see EXAMPLES.md\033[0m"
echo -e "\033[0;36mFor detailed documentation, see README.md\033[0m"
echo ""
echo -e "\033[0;33mNote: Remember to activate the virtual environment:\033[0m"
echo -e "\033[0;37m  source venv/bin/activate\033[0m"
echo ""
