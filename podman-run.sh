#!/bin/bash

# Build and run Listen2Research with Podman

echo "🐋 Building Listen2Research container..."

# Build the container
podman build -t listen2research .

echo "🚀 Starting Listen2Research..."

# Run the container
podman run -d \
  --name listen2research \
  -p 8501:8501 \
  -v ./data:/app/data:Z \
  -v ./audio:/app/audio:Z \
  --restart unless-stopped \
  listen2research

echo "✅ Listen2Research is running!"
echo "🌐 Open your browser and go to: http://localhost:8501"
echo ""
echo "📋 Container management:"
echo "  Stop:    podman stop listen2research"
echo "  Restart: podman restart listen2research"
echo "  Logs:    podman logs listen2research"
echo "  Remove:  podman rm listen2research"
