#!/bin/bash

# Directory definitions
WHISPER_SCRIPT="whisper/baixar.py"
MODEL_DIR="whisper_models"

# Check if model directory exists and is not empty
if [ ! -d "$MODEL_DIR" ] || [ -z "$(ls -A "$MODEL_DIR")" ]; then
    echo "⚠️  Whisper models not found or empty."
    echo "📥  Starting download using $WHISPER_SCRIPT..."
    
    # Check if python3 is available
    if command -v python3 &> /dev/null; then
        # Check if faster_whisper is installed
        python3 -c "import faster_whisper" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "❌  'faster_whisper' library not found."
            echo "    Please install it with: pip install faster-whisper"
            echo "    Or ensure you are in the correct virtual environment."
            exit 1
        fi
        
        python3 "$WHISPER_SCRIPT"
        if [ $? -ne 0 ]; then
            echo "❌  Failed to download models."
            exit 1
        fi
    else
        echo "❌  python3 not found."
        exit 1
    fi
else
    echo "✅  Whisper models found in $MODEL_DIR."
fi

echo "🚀  Starting applications with Docker Compose..."
docker-compose up
