# 📦 Installation Guide

This guide will help you install Notetaker Transcriber on your system.

## 🖥️ System Requirements

### Supported Operating Systems
- **macOS** 10.14+ (Mojave and later)
- **Linux** (Ubuntu 18.04+, CentOS 7+)
- **Windows** 10+ (with WSL recommended)

### Hardware Requirements
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 2GB+ free space for models
- **CPU**: Multi-core processor recommended
- **GPU**: Optional, for custom training

## 🚀 Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/notetaker_transcriber.git
cd notetaker_transcriber
```

### 2. Install Python Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt
```

### 3. Install System Dependencies

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install ffmpeg portaudio
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg portaudio19-dev python3-dev
```

#### CentOS/RHEL
```bash
sudo yum install ffmpeg portaudio-devel python3-devel
```

#### Windows (with WSL)
```bash
# Install WSL2 and Ubuntu
wsl --install

# Then follow Ubuntu instructions above
```

### 4. Verify Installation

```bash
# Test basic functionality
python src/transcribe_m4a.py --help

# Test audio processing
ffmpeg -version
```

## 🔧 Advanced Installation

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Development Installation

```bash
# Clone with development dependencies
git clone https://github.com/yourusername/notetaker_transcriber.git
cd notetaker_transcriber

# Install in development mode
pip install -e .

# Install development tools
pip install -r requirements-dev.txt
```

### Custom Model Training Setup

For custom model training, you'll need additional tools:

```bash
# Install Kaldi (Linux/macOS)
git clone https://github.com/kaldi-asr/kaldi.git
cd kaldi
./tools/extras/check_dependencies.sh
make -j $(nproc)

# Set environment variable
export KALDI_ROOT=/path/to/kaldi
echo 'export KALDI_ROOT=/path/to/kaldi' >> ~/.bashrc
```

## 🐛 Troubleshooting

### Common Issues

#### 1. PortAudio Installation Issues

**macOS:**
```bash
brew install portaudio
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
pip install pyaudio
```

**Linux:**
```bash
sudo apt install portaudio19-dev
pip install pyaudio
```

#### 2. FFmpeg Not Found

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

#### 3. Vosk Model Download Issues

```bash
# Manual model download
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
```

#### 4. Permission Issues

```bash
# Fix permissions
chmod +x src/*.py
chmod +x examples/*.py
```

### Platform-Specific Notes

#### macOS
- Use Homebrew for system dependencies
- M1/M2 Macs: Use Rosetta for some dependencies
- Audio permissions may be required

#### Linux
- Use package manager for system dependencies
- May need to install additional audio libraries
- Check audio device permissions

#### Windows
- WSL2 recommended for best compatibility
- Native Windows installation possible but limited
- Audio device configuration may be required

## ✅ Verification

After installation, verify everything works:

```bash
# Test basic transcription
python src/transcribe_m4a.py --version

# Test audio processing
python -c "import vosk; print('Vosk OK')"
python -c "import pyaudio; print('PyAudio OK')"

# Test model download
python src/enhanced_transcriber.py --help
```

## 📚 Next Steps

After successful installation:

1. **Read the [Quick Start Guide](../README.md#quick-start)**
2. **Try the [Examples](../examples/)**
3. **Learn about [Voice Adaptation](../docs/accuracy_improvement.md#voice-adaptation-strategies)**
4. **Explore [Custom Training](../docs/accuracy_improvement.md#custom-model-training)**

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/notetaker_transcriber/issues)
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Error message
   - Steps to reproduce 