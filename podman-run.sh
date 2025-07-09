#!/bin/bash

# Build and run NaturalReader Clone with Podman

echo "🐋 Building NaturalReader Clone container..."

# Build the container
podman build -t naturalreader-clone .

echo "🚀 Starting NaturalReader Clone..."

# Run the container
podman run -d \
  --name naturalreader-clone \
  -p 8501:8501 \
  -v ./data:/app/data:Z \
  -v ./audio:/app/audio:Z \
  --restart unless-stopped \
  naturalreader-clone

echo "✅ NaturalReader Clone is running!"
echo "🌐 Open your browser and go to: http://localhost:8501"
echo ""
echo "📋 Container management:"
echo "  Stop:    podman stop naturalreader-clone"
echo "  Restart: podman restart naturalreader-clone"
echo "  Logs:    podman logs naturalreader-clone"
echo "  Remove:  podman rm naturalreader-clone"
