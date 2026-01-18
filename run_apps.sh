#!/bin/bash

# Directory definitions
WHISPER_SCRIPT="whisper/baixar.py"
MODEL_DIR="whisper/whisper_models"

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

# Check for SSL certificates
CERTS_DIR="API Python/certs"
if [ ! -f "$CERTS_DIR/cert.pem" ] || [ ! -f "$CERTS_DIR/key.pem" ]; then
    echo "⚠️  SSL certificates not found in $CERTS_DIR."
    echo "🔐 Generating self-signed certificates..."
    
    # Check if python3 is available (reusing check if possible, but good to be safe)
    if command -v python3 &> /dev/null; then
        # Run the generation script from the API Python directory to ensure correct output path
        (cd "API Python" && python3 "scripts/generate_cert.py")
        if [ $? -ne 0 ]; then
             echo "❌  Failed to generate certificates."
             # Not exiting here to allow user to proceed if they really want to, 
             # but warning is clear. Or maybe we should exit? 
             # The plan said "Ensure the script handles the certificate generation before starting Docker containers."
             # Let's exit on failure to be safe.
             exit 1
        fi
    else
         echo "❌  python3 not found. Cannot generate certificates."
         exit 1
    fi
else
    echo "✅  SSL certificates found in $CERTS_DIR."
fi

echo "🚀  Starting applications with Docker Compose..."
docker-compose up
