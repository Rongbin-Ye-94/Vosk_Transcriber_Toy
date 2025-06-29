# Vosk-Based Audio Transcription System

A comprehensive audio transcription system built on top of Vosk, featuring multiple transcription approaches and advanced audio processing capabilities. This is a practice project that built by Rongbin Ye and Jiaqi Chen for the practice and comparison perspective. The infrastructure is build upon Vosk. 
https://github.com/alphacep/vosk-api

This project was originally started as authors were interviewing and intends to transcribe the practices and mock interviews. To get better training results, we intend to transcribe the recordings that we have. As we have a lot of information that is very private and protected, we thought of utilizing the vosk and related framework to transcribe the information for tracking and getting feedback. In the progress, we found out that the outcome is not as good as we expected with limited treated data, hence we added more data treatment. Afterward, we chated and try to further improve the transcribe outcome with some additional control. 

This is a prototype model for further improvement. 


## Features

- **Multiple Transcription Methods**: Basic, enhanced, ensemble, and custom training approaches
- **Audio Preprocessing**: Advanced noise reduction and audio enhancement
- **Voice Adaptation**: Speaker-specific voice profile training
- **Accuracy Comparison**: Tools to compare different transcription methods
- **M4A Support**: Direct transcription of M4A audio files
- **Post-processing**: Intelligent text correction and formatting

## Project Structure

```
├── transcribe_m4a.py              # Basic M4A transcription script
├── enhanced_transcriber.py        # Enhanced transcription with preprocessing
├── ensemble_transcriber.py        # Ensemble method combining multiple approaches
├── advanced_transcriber.py        # Advanced features and configurations
├── custom_training_transcriber.py # Custom model training capabilities
├── compare_transcriptions.py      # Compare different transcription methods
├── sample_audio_1.m4a            # Sample audio file for testing
├── notetaker_transcriber/         # Packaged version of the transcription system
├── vosk-api/                      # Vosk API source code
└── vosk-model-en-us-0.22/         # English language model
```

## Installation

### Prerequisites

- Python 3.7+
- FFmpeg (for audio processing)
- Vosk library

### Setup

1. **Install FFmpeg**:
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

2. **Install Python dependencies**:
   ```bash
   pip install vosk requests
   ```

3. **Download Vosk model** (if not already present):
   ```bash
   # The enhanced transcriber will automatically download models
   python enhanced_transcriber.py
   ```

## Usage

### Basic Transcription

```bash
python transcribe_m4a.py sample_audio_1.m4a
```

### Enhanced Transcription

```bash
python enhanced_transcriber.py sample_audio_1.m4a
```

### Ensemble Transcription

```bash
python ensemble_transcriber.py sample_audio_1.m4a
```

### Compare Different Methods

```bash
python compare_transcriptions.py sample_audio_1.m4a
```

## Advanced Features

### Voice Adaptation

Create a voice profile for better recognition:

```bash
python custom_training_transcriber.py --create-profile sample_audio_1.m4a
```

### Custom Model Training

Train a custom model for specific domains:

```bash
python custom_training_transcriber.py --train-model training_data/
```

## Configuration

### Model Selection

The system supports multiple Vosk models:
- `vosk-model-en-us-0.22` (default, highest accuracy)
- `vosk-model-en-us-0.21`
- `vosk-model-small-en-us-0.15` (faster, smaller)

### Audio Preprocessing

The enhanced transcriber includes:
- High-pass and low-pass filtering
- Noise reduction
- Volume normalization
- Sample rate conversion

## Performance

- **Basic transcription**: ~1-2x real-time
- **Enhanced transcription**: ~2-3x real-time (with preprocessing)
- **Ensemble transcription**: ~3-4x real-time (multiple models)

## Accuracy Improvements

The system includes several accuracy improvement techniques:
- Audio preprocessing and noise reduction
- Post-processing text corrections
- Domain-specific vocabulary
- Speaker adaptation
- Ensemble methods

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg and ensure it's in your PATH
2. **Model download fails**: Check internet connection and try manual download
3. **Audio format issues**: Ensure audio file is supported (M4A, WAV, MP3, etc.)

### Debug Mode

Enable verbose logging:
```bash
python transcribe_m4a.py sample_audio_1.m4a --debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) - Offline speech recognition toolkit
- [Kaldi](https://kaldi-asr.org/) - Speech recognition toolkit
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the accuracy improvement guide
3. Open an issue on GitHub

   
## Contact
Rongbin Ye - rongbin.ye.94@gmail.com 
Jiaqi Chen - ronanchen0901@gmail.com

Project Link: [https://github.com/Rongbin-Ye-94/Arrow_on_Knee](https://github.com/Rongbin-Ye-94/Vosk_Transcriber_Toy)
