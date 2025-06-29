#!/usr/bin/env python3
"""
Voice Adaptation Example for Notetaker Transcriber

This example demonstrates how to create a voice profile and use adaptive transcription.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from custom_training_transcriber import CustomTrainingTranscriber

def main():
    """Voice adaptation example"""
    
    print("🎤 Voice Adaptation Example")
    print("=" * 40)
    
    # Initialize transcriber
    transcriber = CustomTrainingTranscriber()
    
    # Example voice samples (replace with your files)
    voice_samples = [
        "voice_sample1.m4a",
        "voice_sample2.m4a", 
        "voice_sample3.m4a"
    ]
    
    # Check if voice samples exist
    existing_samples = [f for f in voice_samples if os.path.exists(f)]
    
    if not existing_samples:
        print("❌ No voice sample files found.")
        print("Please provide valid audio files for voice profile creation.")
        return
    
    print(f"📁 Found {len(existing_samples)} voice samples")
    
    # Create voice profile
    print("\n🎤 Creating voice profile...")
    profile = transcriber.create_voice_profile(existing_samples)
    
    if profile:
        print(f"✅ Voice profile created with {len(profile['audio_files'])} samples")
        
        # Test adaptive transcription
        test_audio = "test_audio.m4a"
        if os.path.exists(test_audio):
            print(f"\n🎵 Testing adaptive transcription on: {test_audio}")
            result = transcriber.adaptive_transcribe(test_audio, "adaptive_output.txt")
            
            if result:
                print("✅ Adaptive transcription completed!")
                print(f"📄 Output saved to: adaptive_output.txt")
            else:
                print("❌ Adaptive transcription failed.")
        else:
            print(f"\n⚠️  Test audio file '{test_audio}' not found.")
            print("Voice profile created successfully. Use it with new audio files.")
    else:
        print("❌ Failed to create voice profile.")

if __name__ == "__main__":
    main() 