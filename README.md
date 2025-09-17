# 🗣️ Paper Reader

A professional Python Streamlit app that replicates Paper Reader functionality - upload PDFs, view them inline, and have them read aloud with real-time sentence highlighting.

## ✨ Features

- 📄 **PDF Viewer**: Inline PDF display with embedded viewer
- 🧠 **Smart Text Extraction**: Advanced filtering removes headers, figures, references, formulas
- 🔊 **Text-to-Speech**: High-quality Google TTS with natural voice
- 🎯 **Real-time Highlighting**: Shows current, next, and previous sentences
- 📊 **Progress Tracking**: Visual progress bar and reading statistics
- 🎛️ **Reading Controls**: Play, pause, next, reset functionality
- � **Organized Audio**: Audio files organized by PDF document
- 🐋 **Containerized**: Ready for Docker/Podman deployment
- 📱 **Responsive Design**: Works on desktop and mobile

## 🏗️ Architecture

```
naturalreader-clone/
├── app.py                    # Main Streamlit application
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Docker Compose setup
├── podman-run.sh            # Podman deployment script
├── requirements.txt         # Python dependencies
│
├── src/                     # Core modules
│   ├── pdf_utils.py         # PDF processing & viewer
│   ├── text_filter.py       # Smart text cleaning
│   ├── tts_utils.py         # Text-to-speech engine
│   └── sync_utils.py        # Highlighting & timing
│
├── audio/                   # Audio files (organized by PDF)
│   └── {pdf_hash}/
│       └── sentence_*.mp3
│
├── data/                    # PDF storage
└── static/                  # Static assets
```

## 🚀 Quick Start

### Option 1: Container Deployment (Recommended)

#### With Podman:
```bash
# Build and run with Podman
./podman-run.sh

# Or with Podman Compose
./podman-compose.sh
```

#### With Docker:
```bash
# Build and run with Docker
docker build -t naturalreader-clone .
docker run -d -p 8501:8501 -v ./data:/app/data -v ./audio:/app/audio naturalreader-clone

# Or with Docker Compose
docker-compose up --build -d
```

### Option 2: Local Development

#### Quick Setup:
```bash
# Run the setup script
./setup.sh

# Run the app
./run.sh
```

#### Manual Setup:
```bash
# Create virtual environment
python3 -m venv venv

# Install dependencies
./venv/bin/pip install -r requirements.txt

# Download NLTK data
./venv/bin/python -c "import nltk; nltk.download('punkt_tab', quiet=True); nltk.download('punkt', quiet=True)"

# Run the app
./venv/bin/streamlit run app.py
```

### 🌐 Access the App

Open your browser and go to: **http://localhost:8501**

## 🎯 How to Use

1. **Upload PDF**: Click "Upload a PDF" and select your document
2. **View Content**: See the PDF in the left panel and extracted text statistics
3. **Start Reading**: Click "🔊 Start Reading" to begin text-to-speech
4. **Follow Along**: Watch sentence highlighting in the right panel
5. **Control Playback**: Use Pause, Next, or Reset buttons as needed
6. **Track Progress**: Monitor reading progress with the progress bar

## 🛠️ Technical Features

### Smart Text Processing
- **Advanced Filtering**: Removes headers, footers, figures, tables, references
- **Formula Detection**: Skips mathematical formulas and equations
- **URL Filtering**: Removes web links and DOIs
- **Bracket Cleaning**: Filters citation brackets and references
- **Length Validation**: Ensures meaningful sentence lengths

### Audio Management
- **Organized Storage**: Audio files organized by PDF document
- **Duration Estimation**: Smart timing based on word count
- **Background Generation**: Audio created on-demand
- **Automatic Cleanup**: Temporary files cleaned up automatically

### User Interface
- **Split Layout**: PDF viewer alongside text progress
- **Visual Highlighting**: Current, next, and previous sentences
- **Progress Tracking**: Real-time progress bar and statistics
- **Responsive Design**: Works on desktop and mobile devices

## 🐋 Container Management

### Podman Commands
```bash
# Build image
podman build -t naturalreader-clone .

# Run container
podman run -d --name naturalreader-clone -p 8501:8501 naturalreader-clone

# View logs
podman logs naturalreader-clone

# Stop container
podman stop naturalreader-clone

# Remove container
podman rm naturalreader-clone
```

### Docker Commands
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# View logs
docker-compose logs

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## Future Enhancements

- 🎵 Add offline TTS with Piper
- 🎛️ Voice speed/pitch controls
- 💾 Export highlights and notes
- 🌍 Multi-language support
- 📱 Mobile-responsive design
- 🔄 Resume reading from specific position

## Requirements

- Python 3.7+
- Internet connection (for gTTS)
- Modern web browser

## License

Open source - feel free to modify and enhance!
