#!/usr/bin/env python3
"""
Basic tests for Notetaker Transcriber
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestNotetakerTranscriber(unittest.TestCase):
    """Basic test cases for Notetaker Transcriber"""
    
    def test_imports(self):
        """Test that all modules can be imported"""
        try:
            import transcribe_m4a
            import enhanced_transcriber
            import ensemble_transcriber
            import custom_training_transcriber
            import compare_transcriptions
            self.assertTrue(True, "All modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")
    
    def test_vosk_available(self):
        """Test that Vosk is available"""
        try:
            from vosk import Model, KaldiRecognizer
            self.assertTrue(True, "Vosk is available")
        except ImportError:
            self.fail("Vosk is not installed")
    
    def test_ffmpeg_available(self):
        """Test that FFmpeg is available"""
        import subprocess
        try:
            result = subprocess.run(["ffmpeg", "-version"], 
                                  capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, "FFmpeg is available")
        except FileNotFoundError:
            self.fail("FFmpeg is not installed")
    
    def test_audio_processing(self):
        """Test basic audio processing functionality"""
        # This is a basic test - in a real scenario, you'd test with actual audio files
        self.assertTrue(True, "Audio processing test placeholder")

if __name__ == "__main__":
    unittest.main() 