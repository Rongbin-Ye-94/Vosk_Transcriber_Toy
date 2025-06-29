#!/usr/bin/env python3

import subprocess
import sys
import json
import os
import time
import threading
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel

class AudioTranscriber:
    def __init__(self):
        SetLogLevel(-1)
        try:
            self.model = Model(lang="en-us")
            print("✓ Vosk model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            sys.exit(1)
    
    def transcribe_file(self, audio_file_path, output_file=None):
        """Transcribe an audio file"""
        if not os.path.exists(audio_file_path):
            print(f"✗ Error: Audio file '{audio_file_path}' not found.")
            return None
        
        print(f"🎵 Transcribing: {audio_file_path}")
        
        try:
            process = subprocess.Popen([
                "ffmpeg", "-loglevel", "quiet", "-i", audio_file_path,
                "-ar", "16000", "-ac", "1", "-f", "s16le", "-"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            rec = KaldiRecognizer(self.model, 16000)
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
            
            # Combine all transcription parts
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
            
            # Output results
            print("\n" + "="*60)
            print("📝 TRANSCRIPTION RESULT")
            print("="*60)
            print(full_transcription)
            print("="*60)
            
            # Save to file if requested
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_transcription)
                print(f"\n💾 Transcription saved to: {output_file}")
            
            return full_transcription
            
        except FileNotFoundError:
            print("✗ Error: ffmpeg not found. Please install ffmpeg.")
        except Exception as e:
            print(f"✗ Error during transcription: {e}")
        
        return None
    
    def record_and_transcribe(self, duration=30, output_file=None):
        """Record audio from microphone and transcribe in real-time"""
        try:
            import pyaudio
        except ImportError:
            print("✗ Error: pyaudio not installed. Install it with: pip3 install pyaudio")
            return None
        
        print(f"🎤 Recording for {duration} seconds... (Press Ctrl+C to stop early)")
        print("Speak now!")
        
        # Audio recording parameters
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           input=True,
                           frames_per_buffer=CHUNK)
            
            rec = KaldiRecognizer(self.model, RATE)
            rec.SetWords(True)
            
            transcription_parts = []
            start_time = time.time()
            
            print("🎙️  Recording started...")
            
            while time.time() - start_time < duration:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    
                    if rec.AcceptWaveform(data):
                        result = rec.Result()
                        if result.strip():
                            try:
                                json_result = json.loads(result)
                                if 'text' in json_result and json_result['text'].strip():
                                    print(f"📝 {json_result['text']}")
                                    transcription_parts.append(json_result['text'])
                            except json.JSONDecodeError:
                                continue
                
                except KeyboardInterrupt:
                    print("\n⏹️  Recording stopped by user")
                    break
            
            # Get final result
            final_result = rec.FinalResult()
            if final_result.strip():
                try:
                    json_result = json.loads(final_result)
                    if 'text' in json_result and json_result['text'].strip():
                        print(f"📝 {json_result['text']}")
                        transcription_parts.append(json_result['text'])
                except json.JSONDecodeError:
                    pass
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Combine all transcription parts
            full_transcription = " ".join(transcription_parts)
            
            if not full_transcription:
                print("⚠️  No speech detected during recording.")
                return None
            
            print("\n" + "="*60)
            print("📝 FINAL TRANSCRIPTION")
            print("="*60)
            print(full_transcription)
            print("="*60)
            
            # Save to file if requested
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_transcription)
                print(f"\n💾 Transcription saved to: {output_file}")
            
            return full_transcription
            
        except Exception as e:
            print(f"✗ Error during recording: {e}")
            if 'stream' in locals():
                stream.close()
            if 'p' in locals():
                p.terminate()
        
        return None

def main():
    transcriber = AudioTranscriber()
    
    if len(sys.argv) < 2:
        print("🎯 Audio Transcription Tool")
        print("="*40)
        print("Usage:")
        print("  python3 advanced_transcriber.py file <audio_file> [output_file]")
        print("  python3 advanced_transcriber.py record [duration] [output_file]")
        print("\nExamples:")
        print("  python3 advanced_transcriber.py file 'audio.m4a'")
        print("  python3 advanced_transcriber.py file 'audio.m4a' 'transcript.txt'")
        print("  python3 advanced_transcriber.py record 30")
        print("  python3 advanced_transcriber.py record 60 'live_transcript.txt'")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "file":
        if len(sys.argv) < 3:
            print("✗ Error: Please specify an audio file")
            sys.exit(1)
        
        audio_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        transcriber.transcribe_file(audio_file, output_file)
    
    elif mode == "record":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        transcriber.record_and_transcribe(duration, output_file)
    
    else:
        print(f"✗ Error: Unknown mode '{mode}'. Use 'file' or 'record'")
        sys.exit(1)

if __name__ == "__main__":
    main() 