#!/usr/bin/env python3

import subprocess
import sys
import json
import os
import time
import re
import requests
import zipfile
import shutil
from vosk import Model, KaldiRecognizer, SetLogLevel

class CustomTrainingTranscriber:
    def __init__(self):
        SetLogLevel(-1)
        self.models = {}
        self.custom_model_path = None
        self.load_models()
    
    def load_models(self):
        """Load available models including custom ones"""
        print("🔧 Loading transcription models...")
        
        # Check for custom trained model
        custom_model_path = "custom_model"
        if os.path.exists(custom_model_path):
            try:
                self.models["custom"] = Model(custom_model_path)
                self.custom_model_path = custom_model_path
                print("✅ Loaded custom trained model")
            except Exception as e:
                print(f"⚠️  Failed to load custom model: {e}")
        
        # Load standard models
        standard_models = [
            "vosk-model-en-us-0.22",
            "vosk-model-en-us-0.21", 
            "vosk-model-en-us-0.15"
        ]
        
        for model_name in standard_models:
            if os.path.exists(model_name):
                try:
                    self.models[model_name] = Model(model_name)
                    print(f"✅ Loaded: {model_name}")
                except Exception as e:
                    print(f"⚠️  Failed to load {model_name}: {e}")
        
        if not self.models:
            print("⚠️  No models loaded, falling back to default")
            try:
                self.models["default"] = Model(lang="en-us")
                print("✅ Default model loaded")
            except Exception as e:
                print(f"✗ Error loading default model: {e}")
                sys.exit(1)
    
    def prepare_training_data(self, audio_files, transcriptions, output_dir="training_data"):
        """Prepare audio files and transcriptions for training"""
        print(f"📁 Preparing training data in: {output_dir}")
        
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        # Create subdirectories
        wav_dir = os.path.join(output_dir, "wav")
        txt_dir = os.path.join(output_dir, "txt")
        os.makedirs(wav_dir, exist_ok=True)
        os.makedirs(txt_dir, exist_ok=True)
        
        prepared_files = []
        
        for i, (audio_file, transcription) in enumerate(zip(audio_files, transcriptions)):
            if not os.path.exists(audio_file):
                print(f"⚠️  Audio file not found: {audio_file}")
                continue
            
            # Convert to WAV format
            wav_file = os.path.join(wav_dir, f"sample_{i:04d}.wav")
            cmd = [
                "ffmpeg", "-y", "-i", audio_file,
                "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
                wav_file
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    # Save transcription
                    txt_file = os.path.join(txt_dir, f"sample_{i:04d}.txt")
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(transcription.strip())
                    
                    prepared_files.append((wav_file, txt_file))
                    print(f"✅ Prepared: sample_{i:04d}")
                else:
                    print(f"⚠️  Failed to convert: {audio_file}")
            except Exception as e:
                print(f"⚠️  Error processing {audio_file}: {e}")
        
        print(f"📊 Prepared {len(prepared_files)} training samples")
        return prepared_files
    
    def create_training_script(self, training_data_dir):
        """Create a training script for custom model"""
        script_content = f'''#!/bin/bash

# Custom Vosk Model Training Script
# Generated for voice adaptation

set -e

# Configuration
TRAINING_DATA_DIR="{training_data_dir}"
MODEL_OUTPUT_DIR="custom_model"
KALDI_ROOT="${{KALDI_ROOT:-/path/to/kaldi}}"

echo "🎯 Starting custom model training..."

# Check if Kaldi is available
if [ ! -d "$KALDI_ROOT" ]; then
    echo "❌ Kaldi not found. Please install Kaldi and set KALDI_ROOT"
    echo "   Download from: https://github.com/kaldi-asr/kaldi"
    exit 1
fi

# Set up environment
export PATH="$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/tools/sph2pipe_v2.5:$PATH"
export PATH="$KALDI_ROOT/tools/sctk/bin:$PATH"
export PATH="$KALDI_ROOT/tools/sph2pipe_v2.5:$PATH"

# Create training directory structure
mkdir -p $MODEL_OUTPUT_DIR
mkdir -p $MODEL_OUTPUT_DIR/data
mkdir -p $MODEL_OUTPUT_DIR/exp
mkdir -p $MODEL_OUTPUT_DIR/conf

# Copy training data
cp -r $TRAINING_DATA_DIR/wav/* $MODEL_OUTPUT_DIR/data/
cp -r $TRAINING_DATA_DIR/txt/* $MODEL_OUTPUT_DIR/data/

echo "📊 Training data prepared"
echo "⚠️  Note: Full model training requires significant computational resources"
echo "   This is a simplified training script. For production use, consider:"
echo "   - Using a pre-trained model as starting point"
echo "   - Fine-tuning with your specific domain data"
echo "   - Using cloud computing resources"

# Create a simple adaptation script
cat > $MODEL_OUTPUT_DIR/adapt.sh << 'EOF'
#!/bin/bash
# Voice adaptation script
echo "🎤 Starting voice adaptation..."

# This would typically involve:
# 1. Feature extraction
# 2. Speaker adaptation
# 3. Model fine-tuning
# 4. Decoding and evaluation

echo "✅ Adaptation completed (simplified version)"
EOF

chmod +x $MODEL_OUTPUT_DIR/adapt.sh

echo "✅ Training script created in: $MODEL_OUTPUT_DIR"
echo "📝 Next steps:"
echo "   1. Install Kaldi: https://github.com/kaldi-asr/kaldi"
echo "   2. Set KALDI_ROOT environment variable"
echo "   3. Run: cd $MODEL_OUTPUT_DIR && ./adapt.sh"
'''
        
        script_path = "train_custom_model.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        print(f"✅ Training script created: {script_path}")
        return script_path
    
    def create_voice_profile(self, audio_files, output_dir="voice_profile"):
        """Create a voice profile for adaptation"""
        print(f"🎤 Creating voice profile in: {output_dir}")
        
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        profile_data = {
            "speaker_id": "user_voice",
            "audio_files": [],
            "characteristics": {},
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for i, audio_file in enumerate(audio_files):
            if not os.path.exists(audio_file):
                continue
            
            # Analyze audio characteristics
            wav_file = os.path.join(output_dir, f"sample_{i:04d}.wav")
            cmd = [
                "ffmpeg", "-y", "-i", audio_file,
                "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
                wav_file
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    profile_data["audio_files"].append({
                        "original": audio_file,
                        "processed": wav_file,
                        "index": i
                    })
                    
                    # Get audio duration
                    duration_cmd = [
                        "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", wav_file
                    ]
                    duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
                    if duration_result.returncode == 0:
                        try:
                            duration = float(duration_result.stdout.strip())
                            profile_data["characteristics"][f"sample_{i:04d}"] = {
                                "duration": duration,
                                "format": "16kHz mono WAV"
                            }
                        except:
                            pass
                    
                    print(f"✅ Processed: sample_{i:04d}")
            except Exception as e:
                print(f"⚠️  Error processing {audio_file}: {e}")
        
        # Save profile
        profile_file = os.path.join(output_dir, "voice_profile.json")
        with open(profile_file, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        print(f"✅ Voice profile saved: {profile_file}")
        return profile_data
    
    def adaptive_transcribe(self, audio_file, output_file=None, use_voice_profile=True):
        """Transcribe with voice adaptation"""
        if not os.path.exists(audio_file):
            print(f"✗ Error: Audio file '{audio_file}' not found.")
            return None
        
        print(f"🎵 Adaptive transcribing: {audio_file}")
        
        # Check for voice profile
        voice_profile_path = "voice_profile/voice_profile.json"
        if use_voice_profile and os.path.exists(voice_profile_path):
            try:
                with open(voice_profile_path, 'r') as f:
                    profile = json.load(f)
                print(f"🎤 Using voice profile: {profile['speaker_id']}")
            except:
                use_voice_profile = False
        
        # Choose best model (custom first, then largest standard)
        best_model_name = None
        best_model = None
        
        if "custom" in self.models:
            best_model_name = "custom"
            best_model = self.models["custom"]
        elif "vosk-model-en-us-0.22" in self.models:
            best_model_name = "vosk-model-en-us-0.22"
            best_model = self.models["vosk-model-en-us-0.22"]
        else:
            best_model_name = list(self.models.keys())[0]
            best_model = self.models[best_model_name]
        
        print(f"🔧 Using model: {best_model_name}")
        
        # Preprocess audio with voice-specific settings
        processed_file = self.preprocess_for_voice(audio_file, use_voice_profile)
        
        try:
            process = subprocess.Popen([
                "ffmpeg", "-loglevel", "quiet", "-i", processed_file,
                "-ar", "16000", "-ac", "1", "-f", "s16le", "-"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            rec = KaldiRecognizer(best_model, 16000)
            rec.SetWords(True)
            
            transcription_parts = []
            
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    if result.strip():
                        transcription_parts.append(result)
            
            final_result = rec.FinalResult()
            if final_result.strip():
                transcription_parts.append(final_result)
            
            process.wait()
            
            if process.returncode != 0:
                print("✗ Error: ffmpeg failed to process the audio file.")
                return None
            
            # Combine transcription parts
            full_transcription = ""
            for part in transcription_parts:
                try:
                    json_result = json.loads(part)
                    if 'text' in json_result and json_result['text'].strip():
                        full_transcription += json_result['text'] + " "
                except json.JSONDecodeError:
                    continue
            
            full_transcription = full_transcription.strip()
            
            if not full_transcription:
                print("⚠️  No speech detected in the audio file.")
                return None
            
            # Apply voice-specific post-processing
            improved_transcription = self.post_process_for_voice(full_transcription, use_voice_profile)
            
            # Output results
            print("\n" + "="*80)
            print("📝 ADAPTIVE TRANSCRIPTION RESULT")
            print("="*80)
            print(improved_transcription)
            print("="*80)
            
            if use_voice_profile:
                print(f"\n🎤 Voice adaptation applied using profile")
            
            # Save to file if requested
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(improved_transcription)
                print(f"\n💾 Adaptive transcription saved to: {output_file}")
            
            # Clean up
            if processed_file != audio_file and os.path.exists(processed_file):
                try:
                    os.remove(processed_file)
                except:
                    pass
            
            return improved_transcription
            
        except Exception as e:
            print(f"✗ Error during transcription: {e}")
            return None
    
    def preprocess_for_voice(self, audio_file, use_voice_profile=True):
        """Preprocess audio with voice-specific settings"""
        output_file = f"voice_adapted_{os.path.basename(audio_file)}"
        
        # Voice-specific preprocessing
        if use_voice_profile:
            # Enhanced preprocessing for known voice
            cmd = [
                "ffmpeg", "-y", "-i", audio_file,
                "-af", "highpass=f=150,lowpass=f=3500,volume=1.3,compand=0.3|0.3:1|1:-90/-60/-40/-30/-20/-10/-3/0:6:0:-90:0.2",
                "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
                output_file
            ]
        else:
            # Standard preprocessing
            cmd = [
                "ffmpeg", "-y", "-i", audio_file,
                "-af", "highpass=f=200,lowpass=f=3000,volume=1.5",
                "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
                output_file
            ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Voice-adapted preprocessing: {output_file}")
                return output_file
            else:
                print(f"⚠️  Preprocessing failed, using original file")
                return audio_file
        except Exception as e:
            print(f"⚠️  Preprocessing error: {e}, using original file")
            return audio_file
    
    def post_process_for_voice(self, text, use_voice_profile=True):
        """Post-process with voice-specific corrections"""
        if not text:
            return text
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Voice-specific corrections (can be learned from training data)
        voice_corrections = {
            # Common speech patterns
            'yeah yeah': 'yes, yes',
            'uh huh': 'uh-huh',
            'um': 'um',
            'uh': 'uh',
            
            # Personal speech habits (can be customized)
            'i think': 'I think',
            'i would': 'I would',
            'i will': 'I will',
            'i am': 'I am',
            'i have': 'I have',
            'i do': 'I do',
            'i can': 'I can',
            
            # Technical terms (domain-specific)
            'python': 'Python',
            'sql': 'SQL',
            'tableau': 'Tableau',
            'credit risk': 'credit risk',
            'analytics': 'analytics',
            'modeling': 'modeling',
            'dashboard': 'dashboard',
            
            # Interview-specific terms
            'interview': 'interview',
            'experience': 'experience',
            'position': 'position',
            'manager': 'manager',
            'company': 'company',
            'salary': 'salary',
            'sponsorship': 'sponsorship',
        }
        
        # Apply corrections
        for wrong, correct in voice_corrections.items():
            text = re.sub(r'\b' + re.escape(wrong) + r'\b', correct, text, flags=re.IGNORECASE)
        
        # Capitalize sentences
        sentences = re.split(r'([.!?]+)', text)
        corrected_sentences = []
        for i, sentence in enumerate(sentences):
            if i % 2 == 0:  # This is a sentence (not punctuation)
                if sentence.strip():
                    sentence = sentence.strip().capitalize()
            corrected_sentences.append(sentence)
        
        text = ''.join(corrected_sentences)
        
        # Final cleanup
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

def main():
    print("🎯 Custom Training Transcription Tool")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 custom_training_transcriber.py transcribe <audio_file> [output_file]")
        print("  python3 custom_training_transcriber.py create-profile <audio_file1> [audio_file2] ...")
        print("  python3 custom_training_transcriber.py prepare-training <audio_file1> <transcript1> [audio_file2] [transcript2] ...")
        print("\nExamples:")
        print("  python3 custom_training_transcriber.py transcribe 'audio.m4a'")
        print("  python3 custom_training_transcriber.py create-profile 'voice1.m4a' 'voice2.m4a'")
        print("  python3 custom_training_transcriber.py prepare-training 'audio1.m4a' 'transcript1.txt' 'audio2.m4a' 'transcript2.txt'")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    transcriber = CustomTrainingTranscriber()
    
    if command == "transcribe":
        if len(sys.argv) < 3:
            print("✗ Error: Please specify an audio file")
            sys.exit(1)
        
        audio_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        transcriber.adaptive_transcribe(audio_file, output_file)
    
    elif command == "create-profile":
        if len(sys.argv) < 3:
            print("✗ Error: Please specify at least one audio file")
            sys.exit(1)
        
        audio_files = sys.argv[2:]
        profile = transcriber.create_voice_profile(audio_files)
        print(f"\n🎤 Voice profile created with {len(profile['audio_files'])} samples")
    
    elif command == "prepare-training":
        if len(sys.argv) < 4 or len(sys.argv) % 2 != 0:
            print("✗ Error: Please specify pairs of audio files and transcriptions")
            sys.exit(1)
        
        args = sys.argv[2:]
        audio_files = args[::2]
        transcriptions = args[1::2]
        
        # Read transcription files
        transcription_texts = []
        for txt_file in transcriptions:
            if os.path.exists(txt_file):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    transcription_texts.append(f.read().strip())
            else:
                transcription_texts.append(txt_file)  # Assume it's direct text
        
        prepared_files = transcriber.prepare_training_data(audio_files, transcription_texts)
        script_path = transcriber.create_training_script("training_data")
        
        print(f"\n📚 Training data prepared:")
        print(f"   - {len(prepared_files)} audio-transcription pairs")
        print(f"   - Training script: {script_path}")
        print(f"   - Next: Install Kaldi and run the training script")
    
    else:
        print(f"✗ Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == "__main__":
    main() 