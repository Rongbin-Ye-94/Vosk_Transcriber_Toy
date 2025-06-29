#!/usr/bin/env python3
"""
Example usage of the Vosk-based transcription system.

This script demonstrates how to use different transcription methods
with the provided audio files.
"""

import os
import sys
from pathlib import Path

def run_basic_transcription():
    """Run basic transcription on sample audio."""
    print("=" * 60)
    print("BASIC TRANSCRIPTION EXAMPLE")
    print("=" * 60)
    
    audio_file = "sample_audio_1.m4a"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found.")
        print("Please ensure you have a sample audio file available.")
        return
    
    print(f"🎵 Transcribing: {audio_file}")
    print("📝 Running basic transcription...")
    
    # Import and run basic transcription
    try:
        from transcribe_m4a import transcribe_audio
        result = transcribe_audio(audio_file, "basic_transcription.txt")
        if result:
            print("✅ Basic transcription completed!")
            print(f"📄 Results saved to: basic_transcription.txt")
        else:
            print("❌ Basic transcription failed.")
    except Exception as e:
        print(f"❌ Error during basic transcription: {e}")

def run_enhanced_transcription():
    """Run enhanced transcription on sample audio."""
    print("\n" + "=" * 60)
    print("ENHANCED TRANSCRIPTION EXAMPLE")
    print("=" * 60)
    
    audio_file = "sample_audio_1.m4a"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found.")
        return
    
    print(f"🎵 Transcribing: {audio_file}")
    print("📝 Running enhanced transcription with preprocessing...")
    
    # Import and run enhanced transcription
    try:
        from enhanced_transcriber import EnhancedAudioTranscriber
        transcriber = EnhancedAudioTranscriber()
        result = transcriber.transcribe_with_confidence(audio_file, "enhanced_transcription.txt")
        if result:
            print("✅ Enhanced transcription completed!")
            print(f"📄 Results saved to: enhanced_transcription.txt")
        else:
            print("❌ Enhanced transcription failed.")
    except Exception as e:
        print(f"❌ Error during enhanced transcription: {e}")

def run_ensemble_transcription():
    """Run ensemble transcription on sample audio."""
    print("\n" + "=" * 60)
    print("ENSEMBLE TRANSCRIPTION EXAMPLE")
    print("=" * 60)
    
    audio_file = "sample_audio_1.m4a"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found.")
        return
    
    print(f"🎵 Transcribing: {audio_file}")
    print("📝 Running ensemble transcription...")
    
    # Import and run ensemble transcription
    try:
        from ensemble_transcriber import EnsembleTranscriber
        transcriber = EnsembleTranscriber()
        result = transcriber.transcribe_ensemble(audio_file, "ensemble_transcription.txt")
        if result:
            print("✅ Ensemble transcription completed!")
            print(f"📄 Results saved to: ensemble_transcription.txt")
        else:
            print("❌ Ensemble transcription failed.")
    except Exception as e:
        print(f"❌ Error during ensemble transcription: {e}")

def compare_methods():
    """Compare different transcription methods."""
    print("\n" + "=" * 60)
    print("COMPARISON EXAMPLE")
    print("=" * 60)
    
    audio_file = "sample_audio_1.m4a"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found.")
        return
    
    print(f"🎵 Comparing transcription methods for: {audio_file}")
    print("📝 Running comparison...")
    
    # Import and run comparison
    try:
        from compare_transcriptions import compare_transcription_methods
        results = compare_transcription_methods(audio_file)
        if results:
            print("✅ Comparison completed!")
            print("📊 Results:")
            for method, result in results.items():
                print(f"   {method}: {len(result)} characters")
        else:
            print("❌ Comparison failed.")
    except Exception as e:
        print(f"❌ Error during comparison: {e}")

def main():
    """Main function to run all examples."""
    print("🎤 VOSK TRANSCRIPTION SYSTEM - EXAMPLE USAGE")
    print("=" * 60)
    
    # Check if sample audio exists
    audio_file = "sample_audio_1.m4a"
    if not os.path.exists(audio_file):
        print(f"⚠️  Sample audio file '{audio_file}' not found.")
        print("Please add a sample audio file to test the transcription system.")
        print("You can use any M4A, WAV, or MP3 file.")
        return
    
    # Run examples
    run_basic_transcription()
    run_enhanced_transcription()
    run_ensemble_transcription()
    compare_methods()
    
    print("\n" + "=" * 60)
    print("✅ ALL EXAMPLES COMPLETED!")
    print("=" * 60)
    print("📁 Check the generated text files for transcription results.")
    print("📖 For more information, see the README.md file.")

if __name__ == "__main__":
    main() 