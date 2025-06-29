#!/usr/bin/env python3
"""
Quick Start Script for Notetaker Transcriber

This script provides an easy way to get started with transcription.
"""

import sys
import os
import argparse

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Quick start interface"""
    
    parser = argparse.ArgumentParser(
        description="Notetaker Transcriber - Quick Start",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quick_start.py transcribe audio.m4a
  python quick_start.py enhance audio.m4a output.txt
  python quick_start.py ensemble audio.m4a
  python quick_start.py voice-profile voice1.m4a voice2.m4a
  python quick_start.py compare audio.m4a
        """
    )
    
    parser.add_argument(
        "action",
        choices=["transcribe", "enhance", "ensemble", "voice-profile", "compare"],
        help="Action to perform"
    )
    
    parser.add_argument(
        "files",
        nargs="+",
        help="Audio files to process"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file (optional)"
    )
    
    args = parser.parse_args()
    
    print("🎯 Notetaker Transcriber - Quick Start")
    print("=" * 50)
    
    # Check if files exist
    for file in args.files:
        if not os.path.exists(file):
            print(f"❌ File not found: {file}")
            return
    
    try:
        if args.action == "transcribe":
            from transcribe_m4a import transcribe_audio
            output = args.output or "transcription.txt"
            print(f"📝 Basic transcription: {args.files[0]} -> {output}")
            result = transcribe_audio(args.files[0], output)
            
        elif args.action == "enhance":
            from enhanced_transcriber import EnhancedAudioTranscriber
            output = args.output or "enhanced_transcription.txt"
            print(f"🚀 Enhanced transcription: {args.files[0]} -> {output}")
            transcriber = EnhancedAudioTranscriber()
            result = transcriber.transcribe_with_confidence(args.files[0], output)
            
        elif args.action == "ensemble":
            from ensemble_transcriber import EnsembleAudioTranscriber
            output = args.output or "ensemble_transcription.txt"
            print(f"🎯 Ensemble transcription: {args.files[0]} -> {output}")
            transcriber = EnsembleAudioTranscriber()
            result = transcriber.ensemble_transcribe(args.files[0], output)
            
        elif args.action == "voice-profile":
            from custom_training_transcriber import CustomTrainingTranscriber
            print(f"🎤 Creating voice profile from {len(args.files)} files")
            transcriber = CustomTrainingTranscriber()
            result = transcriber.create_voice_profile(args.files)
            
        elif args.action == "compare":
            from compare_transcriptions import main as compare_main
            print(f"📊 Comparing transcription methods for: {args.files[0]}")
            # Temporarily modify sys.argv for the comparison script
            original_argv = sys.argv
            sys.argv = ["compare_transcriptions.py", args.files[0]]
            compare_main()
            sys.argv = original_argv
            result = True
            
        if result:
            print("✅ Operation completed successfully!")
        else:
            print("❌ Operation failed.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
        print("   brew install ffmpeg portaudio  # on macOS")

if __name__ == "__main__":
    main() 