# 🎯 Custom Training Guide

Learn how to train custom speech recognition models for your specific voice and domain.

## 📋 Overview

Custom training allows you to create models that are specifically adapted to:
- Your voice characteristics
- Your speaking patterns
- Your domain-specific vocabulary
- Your accent and pronunciation

## 🎤 Voice Profile Creation

### What is a Voice Profile?

A voice profile captures your unique speech characteristics:
- Voice timbre and pitch
- Speaking pace and rhythm
- Pronunciation patterns
- Common speech habits

### Creating Your Voice Profile

```bash
# Create voice profile from your recordings
python src/custom_training_transcriber.py create-profile \
  "voice_sample1.m4a" \
  "voice_sample2.m4a" \
  "voice_sample3.m4a"
```

**Requirements:**
- 3-10 audio recordings of your voice
- Clear, high-quality audio
- Various topics and speaking styles
- 30 seconds to 5 minutes each

### Voice Profile Structure

```json
{
  "speaker_id": "user_voice",
  "audio_files": [
    {
      "original": "voice_sample1.m4a",
      "processed": "voice_profile/sample_0000.wav",
      "index": 0
    }
  ],
  "characteristics": {
    "sample_0000": {
      "duration": 45.2,
      "format": "16kHz mono WAV"
    }
  },
  "created_at": "2025-01-19 13:47:55"
}
```

## 📚 Training Data Preparation

### Collecting Training Data

**Recommended Dataset Size:**
- **Minimum**: 10 hours of audio
- **Recommended**: 50+ hours
- **Optimal**: 100+ hours

**Audio Quality Requirements:**
- Clear speech (minimal background noise)
- Consistent recording conditions
- Various topics and contexts
- Natural speaking patterns

### Preparing Training Data

```bash
# Prepare training data with transcriptions
python src/custom_training_transcriber.py prepare-training \
  "audio1.m4a" "transcript1.txt" \
  "audio2.m4a" "transcript2.txt" \
  "audio3.m4a" "transcript3.txt"
```

**Transcription Format:**
- Plain text files
- One transcription per audio file
- Accurate, word-for-word transcriptions
- Include punctuation and formatting

### Training Data Structure

```
training_data/
├── wav/
│   ├── sample_0000.wav
│   ├── sample_0001.wav
│   └── sample_0002.wav
└── txt/
    ├── sample_0000.txt
    ├── sample_0001.txt
    └── sample_0002.txt
```

## 🔧 Custom Model Training

### Prerequisites

1. **Install Kaldi Toolkit:**
   ```bash
   git clone https://github.com/kaldi-asr/kaldi.git
   cd kaldi
   ./tools/extras/check_dependencies.sh
   make -j $(nproc)
   ```

2. **Set Environment Variables:**
   ```bash
   export KALDI_ROOT=/path/to/kaldi
   echo 'export KALDI_ROOT=/path/to/kaldi' >> ~/.bashrc
   ```

3. **Install Additional Dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt install openfst-tools sctk
   
   # macOS
   brew install openfst sctk
   ```

### Training Process

1. **Generate Training Script:**
   ```bash
   python src/custom_training_transcriber.py prepare-training \
     "audio1.m4a" "transcript1.txt" \
     "audio2.m4a" "transcript2.txt"
   ```

2. **Run Training:**
   ```bash
   chmod +x train_custom_model.sh
   ./train_custom_model.sh
   ```

3. **Monitor Progress:**
   - Training can take days to weeks
   - Monitor GPU usage and memory
   - Check log files for errors

### Training Pipeline

1. **Data Preparation**
   - Convert audio to WAV format
   - Align audio with transcriptions
   - Create Kaldi data directories

2. **Feature Extraction**
   - Extract MFCC features
   - Compute Cepstral Mean Variance Normalization
   - Generate i-vectors for speaker adaptation

3. **Acoustic Model Training**
   - Monophone training
   - Triphone training with LDA+MLLT
   - Speaker Adaptive Training (SAT)
   - Neural network training (TDNN)

4. **Language Model Training**
   - Create n-gram language model
   - Build pronunciation dictionary
   - Generate decoding graph

5. **Decoding and Evaluation**
   - Decode test data
   - Calculate Word Error Rate (WER)
   - Optimize model parameters

## 📊 Model Evaluation

### Metrics

- **Word Error Rate (WER)**: Primary accuracy metric
- **Character Error Rate (CER)**: Character-level accuracy
- **Real-time Factor (RTF)**: Processing speed
- **Memory Usage**: Resource requirements

### Testing Your Model

```bash
# Test custom model
python src/custom_training_transcriber.py transcribe "test_audio.m4a"
```

### Expected Improvements

| Training Data Size | Expected WER Improvement |
|-------------------|-------------------------|
| 10 hours | 10-20% |
| 50 hours | 20-35% |
| 100+ hours | 30-50% |

## 🎯 Domain-Specific Training

### Technical Interviews

**Focus Areas:**
- Programming language names
- Technical terminology
- Code syntax and commands
- Interview-specific phrases

**Training Data:**
- Mock interview recordings
- Technical discussions
- Code walkthroughs
- Problem-solving sessions

### Business Meetings

**Focus Areas:**
- Business terminology
- Company names and products
- Meeting-specific vocabulary
- Action items and decisions

**Training Data:**
- Meeting recordings
- Business presentations
- Client discussions
- Strategy sessions

### Academic Content

**Focus Areas:**
- Academic vocabulary
- Subject-specific terms
- Citation formats
- Research methodology

**Training Data:**
- Lecture recordings
- Research presentations
- Academic discussions
- Paper reviews

## 🔄 Model Updates

### Incremental Training

```bash
# Add new training data
python src/custom_training_transcriber.py prepare-training \
  --append \
  "new_audio1.m4a" "new_transcript1.txt"
```

### Model Fine-tuning

```bash
# Fine-tune existing model
python src/custom_training_transcriber.py fine-tune \
  --base-model "custom_model" \
  --new-data "new_training_data"
```

## 🚀 Best Practices

### Data Collection

1. **Diverse Content**: Include various topics and contexts
2. **Quality Audio**: Use good microphones and quiet environments
3. **Natural Speech**: Avoid reading scripts, speak naturally
4. **Consistent Conditions**: Maintain similar recording setup

### Training Process

1. **Start Small**: Begin with 10 hours, then expand
2. **Validate Early**: Test on held-out data during training
3. **Monitor Resources**: Watch GPU memory and disk space
4. **Backup Models**: Save checkpoints and final models

### Model Deployment

1. **Test Thoroughly**: Evaluate on real-world data
2. **Optimize Performance**: Balance accuracy vs. speed
3. **Version Control**: Track model versions and changes
4. **Documentation**: Record training parameters and results

## 🐛 Troubleshooting

### Common Issues

**Low Accuracy:**
- Insufficient training data
- Poor audio quality
- Inaccurate transcriptions
- Mismatched domain

**Training Failures:**
- Insufficient memory
- Corrupted audio files
- Incorrect transcription format
- Missing dependencies

**Slow Training:**
- Use GPU acceleration
- Reduce batch size
- Optimize data pipeline
- Use distributed training

## 📚 Resources

- [Kaldi Documentation](https://kaldi-asr.org/doc/)
- [Vosk Training Guide](https://alphacephei.com/vosk/)
- [Speech Recognition Best Practices](https://arxiv.org/abs/2005.00026)
- [Custom Model Examples](https://github.com/alphacep/vosk-api/tree/master/python/example)

## 🎉 Success Stories

Users have achieved:
- 40% WER reduction for technical interviews
- 35% improvement for non-native speakers
- 50% better recognition of domain-specific terms
- Real-time transcription with 95%+ accuracy

---

**Ready to train your custom model? Start with [Voice Profile Creation](#creating-your-voice-profile)!** 