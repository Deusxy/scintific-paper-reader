#!/bin/bash

# Build and run with Podman Compose

echo "🐋 Building and running NaturalReader Clone with Podman Compose..."

# Build and run with podman-compose
podman-compose up --build -d

echo "✅ NaturalReader Clone is running!"
echo "🌐 Open your browser and go to: http://localhost:8501"
echo ""
echo "📋 Compose management:"
echo "  Stop:    podman-compose down"
echo "  Restart: podman-compose restart"
echo "  Logs:    podman-compose logs"
echo "  Rebuild: podman-compose up --build -d"
