#!/usr/bin/env python3

import subprocess
import sys
import json
import os
from vosk import Model, KaldiRecognizer, SetLogLevel

def transcribe_audio(audio_file_path, output_file=None):
    """Transcribe an audio file using Vosk"""
    
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file '{audio_file_path}' not found.")
        return
    
    # Initialize Vosk
    SetLogLevel(-1)
    
    try:
        model = Model(lang="en-us")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Set up recognizer
    SAMPLE_RATE = 16000
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)
    
    print(f"Transcribing: {audio_file_path}")
    
    try:
        process = subprocess.Popen([
            "ffmpeg", "-loglevel", "quiet", "-i", audio_file_path,
            "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
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
            print("Error: ffmpeg failed to process the audio file.")
            return
        
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
            print("No speech detected in the audio file.")
            return
        
        print("\n" + "="*50)
        print("TRANSCRIPTION RESULT")
        print("="*50)
        print(full_transcription)
        print("="*50)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_transcription)
            print(f"\nTranscription saved to: {output_file}")
        
        return full_transcription
        
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
    except Exception as e:
        print(f"Error during transcription: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_m4a.py <audio_file> [output_file]")
        print("Example: python3 transcribe_m4a.py 'sample_audio_1.m4a'")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    transcribe_audio(audio_file, output_file)

if __name__ == "__main__":
    main() 