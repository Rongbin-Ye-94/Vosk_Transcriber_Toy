#!/usr/bin/env python3
"""
Basic Usage Example for Notetaker Transcriber

This example demonstrates the basic usage of the transcription system.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from transcribe_m4a import transcribe_audio

def main():
    """Basic transcription example"""
    
    # Example audio file (replace with your file)
    audio_file = "example_audio.m4a"
    
    print("🎯 Basic Transcription Example")
    print("=" * 40)
    
    # Check if audio file exists
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found.")
        print("Please provide a valid audio file path.")
        return
    
    # Perform transcription
    print(f"📝 Transcribing: {audio_file}")
    result = transcribe_audio(audio_file, "basic_output.txt")
    
    if result:
        print("✅ Transcription completed successfully!")
        print(f"📄 Output saved to: basic_output.txt")
    else:
        print("❌ Transcription failed.")

if __name__ == "__main__":
    main() 