#!/usr/bin/env python3

import subprocess
import sys
import json
import os
import time
import re
import requests
import zipfile
from vosk import Model, KaldiRecognizer, SetLogLevel

class EnsembleAudioTranscriber:
    def __init__(self):
        SetLogLevel(-1)
        self.models = {}
        self.load_models()
    
    def download_model(self, model_name):
        """Download a specific Vosk model"""
        model_urls = {
            "vosk-model-en-us-0.22": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip",
            "vosk-model-en-us-0.21": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.21.zip",
            "vosk-model-en-us-0.15": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.15.zip",
            "vosk-model-small-en-us-0.15": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        }
        
        if model_name not in model_urls:
            print(f"✗ Error: Model '{model_name}' not found")
            return False
        
        if os.path.exists(model_name):
            print(f"✓ Model '{model_name}' already exists")
            return True
        
        print(f"📥 Downloading model: {model_name}")
        try:
            response = requests.get(model_urls[model_name], stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(f"{model_name}.zip", 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r📥 Download progress: {percent:.1f}%", end='', flush=True)
            
            print(f"\n📦 Extracting {model_name}...")
            with zipfile.ZipFile(f"{model_name}.zip", 'r') as zip_ref:
                zip_ref.extractall('.')
            
            os.remove(f"{model_name}.zip")
            print(f"✅ Model '{model_name}' ready!")
            return True
            
        except Exception as e:
            print(f"✗ Error downloading model: {e}")
            return False
    
    def load_models(self):
        """Load multiple Vosk models for ensemble"""
        model_names = [
            "vosk-model-en-us-0.22",  # Largest, most accurate
            "vosk-model-en-us-0.21",  # Large, accurate
            "vosk-model-en-us-0.15"   # Medium
        ]
        
        print("🔧 Loading ensemble models...")
        
        for model_name in model_names:
            try:
                if not os.path.exists(model_name):
                    if not self.download_model(model_name):
                        continue
                
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
    
    def create_audio_variations(self, input_file):
        """Create audio variations for better recognition"""
        variations = []
        base_name = os.path.splitext(input_file)[0]
        
        # Variation 1: Normal preprocessing
        var1 = f"{base_name}_var1.wav"
        cmd1 = [
            "ffmpeg", "-y", "-i", input_file,
            "-af", "highpass=f=200,lowpass=f=3000,volume=1.5",
            "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
            var1
        ]
        
        # Variation 2: Different filtering
        var2 = f"{base_name}_var2.wav"
        cmd2 = [
            "ffmpeg", "-y", "-i", input_file,
            "-af", "highpass=f=150,lowpass=f=3500,volume=1.2,compand=0.3|0.3:1|1:-90/-60/-40/-30/-20/-10/-3/0:6:0:-90:0.2",
            "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
            var2
        ]
        
        # Variation 3: Noise reduction
        var3 = f"{base_name}_var3.wav"
        cmd3 = [
            "ffmpeg", "-y", "-i", input_file,
            "-af", "anlmdn=s=7:p=0.002:r=0.01,highpass=f=300,lowpass=f=2800,volume=1.3",
            "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
            var3
        ]
        
        variations_commands = [cmd1, cmd2, cmd3]
        variation_files = [var1, var2, var3]
        
        for i, (cmd, var_file) in enumerate(zip(variations_commands, variation_files)):
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    variations.append(var_file)
                    print(f"✅ Created variation {i+1}: {var_file}")
                else:
                    print(f"⚠️  Failed to create variation {i+1}")
            except Exception as e:
                print(f"⚠️  Error creating variation {i+1}: {e}")
        
        return variations
    
    def transcribe_with_model(self, audio_file, model_name, model):
        """Transcribe audio with a specific model"""
        try:
            process = subprocess.Popen([
                "ffmpeg", "-loglevel", "quiet", "-i", audio_file,
                "-ar", "16000", "-ac", "1", "-f", "s16le", "-"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            rec = KaldiRecognizer(model, 16000)
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
            
            return full_transcription.strip()
            
        except Exception as e:
            print(f"⚠️  Error with model {model_name}: {e}")
            return None
    
    def ensemble_transcribe(self, audio_file, output_file=None):
        """Perform ensemble transcription using multiple models and audio variations"""
        if not os.path.exists(audio_file):
            print(f"✗ Error: Audio file '{audio_file}' not found.")
            return None
        
        print(f"🎵 Ensemble transcribing: {audio_file}")
        print(f"🔧 Using {len(self.models)} models")
        
        # Create audio variations
        print("🎛️  Creating audio variations...")
        variations = self.create_audio_variations(audio_file)
        if not variations:
            variations = [audio_file]  # Fallback to original
        
        # Add original file to variations
        if audio_file not in variations:
            variations.append(audio_file)
        
        all_transcriptions = []
        
        # Transcribe with each model and variation
        for model_name, model in self.models.items():
            print(f"\n🔍 Using model: {model_name}")
            
            for i, variation in enumerate(variations):
                print(f"  📝 Processing variation {i+1}/{len(variations)}...")
                
                transcription = self.transcribe_with_model(variation, model_name, model)
                if transcription:
                    all_transcriptions.append({
                        'model': model_name,
                        'variation': i+1,
                        'text': transcription
                    })
                    print(f"    ✅ Got transcription ({len(transcription)} chars)")
                else:
                    print(f"    ⚠️  No transcription")
        
        if not all_transcriptions:
            print("✗ Error: No transcriptions generated")
            return None
        
        # Analyze and combine transcriptions
        print(f"\n🔍 Analyzing {len(all_transcriptions)} transcriptions...")
        
        # Find the best transcription (longest and most coherent)
        best_transcription = self.select_best_transcription(all_transcriptions)
        
        # Post-process the best transcription
        improved_transcription = self.post_process_transcription(best_transcription)
        
        # Output results
        print("\n" + "="*80)
        print("📝 ENSEMBLE TRANSCRIPTION RESULT")
        print("="*80)
        print(improved_transcription)
        print("="*80)
        
        # Show ensemble statistics
        print(f"\n📊 ENSEMBLE STATISTICS:")
        print(f"- Models used: {len(self.models)}")
        print(f"- Audio variations: {len(variations)}")
        print(f"- Total transcriptions: {len(all_transcriptions)}")
        print(f"- Best model: {best_transcription.get('model', 'unknown')}")
        
        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(improved_transcription)
            print(f"\n💾 Ensemble transcription saved to: {output_file}")
        
        # Clean up variation files
        for variation in variations:
            if variation != audio_file and os.path.exists(variation):
                try:
                    os.remove(variation)
                except:
                    pass
        
        return improved_transcription
    
    def select_best_transcription(self, transcriptions):
        """Select the best transcription from multiple results"""
        if not transcriptions:
            return None
        
        # Score each transcription
        scored_transcriptions = []
        
        for trans in transcriptions:
            text = trans['text']
            score = 0
            
            # Length score (prefer longer transcriptions)
            score += len(text) * 0.1
            
            # Coherence score (prefer transcriptions with fewer repeated words)
            words = text.lower().split()
            unique_words = len(set(words))
            if len(words) > 0:
                coherence = unique_words / len(words)
                score += coherence * 100
            
            # Quality indicators
            if 'python' in text.lower():
                score += 50  # Technical terms
            if 'credit' in text.lower():
                score += 30
            if 'experience' in text.lower():
                score += 20
            if 'interview' in text.lower():
                score += 20
            
            # Penalize very short transcriptions
            if len(text) < 100:
                score -= 50
            
            scored_transcriptions.append((score, trans))
        
        # Sort by score and return the best
        scored_transcriptions.sort(reverse=True)
        return scored_transcriptions[0][1]
    
    def post_process_transcription(self, transcription_data):
        """Post-process the best transcription"""
        if not transcription_data or 'text' not in transcription_data:
            return ""
        
        text = transcription_data['text']
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Common corrections for interview context
        corrections = {
            'yeah yeah': 'yes, yes',
            'uh huh': 'uh-huh',
            'i think': 'I think',
            'i would': 'I would',
            'i will': 'I will',
            'i am': 'I am',
            'i have': 'I have',
            'i do': 'I do',
            'i can': 'I can',
            'python py': 'Python, Py',
            'py spark': 'PySpark',
            'sql': 'SQL',
            'tableau': 'Tableau',
            'synchrony': 'Synchrony',
            'discover': 'Discover',
            'paypal': 'PayPal',
            'credit risk': 'credit risk',
            'modeling': 'modeling',
            'analytics': 'analytics',
            'dashboard': 'dashboard',
            'probability': 'probability',
            'exposure': 'exposure',
            'sponsorship': 'sponsorship',
            'interview': 'interview',
            'position': 'position',
            'experience': 'experience',
            'technical': 'technical',
            'methodology': 'methodology',
            'leadership': 'leadership',
            'operations': 'operations',
            'strategy': 'strategy',
            'industry': 'industry',
            'finance': 'finance',
            'banking': 'banking',
            'analytical': 'analytical',
            'insights': 'insights',
            'managers': 'managers',
            'leaders': 'leaders',
            'decision': 'decision',
            'development': 'development',
            'current': 'current',
            'previous': 'previous',
            'building': 'building',
            'delivering': 'delivering',
            'reports': 'reports',
            'regarding': 'regarding',
            'analysis': 'analysis',
            'potential': 'potential',
            'similar': 'similar',
            'based': 'based',
            'role': 'role',
            'there': 'there',
            'currently': 'currently',
            'one': 'one',
            'first year': 'first year',
            'market': 'market',
            'ranges': 'ranges',
            'salary': 'salary',
            'hundred': 'hundred',
            'thousand': 'thousand',
            'thirty': 'thirty',
            'five': 'five',
            'above': 'above',
            'further': 'further',
            'talk': 'talk',
            'about': 'about',
            'interviewing': 'interviewing',
            'company': 'company',
            'second round': 'second round',
            'coding': 'coding',
            'available': 'available',
            'march': 'March',
            'six': 'six',
            'seven': 'seven',
            'eleven': 'eleven',
            'twelve': 'twelve',
            'four': 'four',
            'pm': 'PM',
            'am': 'AM',
            'cst': 'CST',
            'preferred': 'preferred',
            'time': 'time',
            'entire': 'entire',
            'day': 'day',
            'backfill': 'backfill',
            'expansion': 'expansion',
            'follow up': 'follow up',
            'question': 'question',
            'manager': 'manager',
            'accommodating': 'accommodating',
            'thank you': 'thank you',
        }
        
        # Apply corrections
        for wrong, correct in corrections.items():
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
    print("🎯 Ensemble Audio Transcription Tool")
    print("="*50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 ensemble_transcriber.py <audio_file> [output_file]")
        print("\nThis tool uses multiple models and audio variations for maximum accuracy.")
        print("\nExamples:")
        print("  python3 ensemble_transcriber.py 'audio.m4a'")
        print("  python3 ensemble_transcriber.py 'audio.m4a' 'ensemble_transcript.txt'")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    transcriber = EnsembleAudioTranscriber()
    transcriber.ensemble_transcribe(audio_file, output_file)

if __name__ == "__main__":
    main() 