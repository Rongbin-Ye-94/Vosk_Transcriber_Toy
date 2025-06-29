#!/usr/bin/env python3
"""
Accuracy Comparison Example for Notetaker Transcriber

This example demonstrates how to compare different transcription methods.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from compare_transcriptions import run_transcription, analyze_transcription

def main():
    """Accuracy comparison example"""
    
    print("📊 Accuracy Comparison Example")
    print("=" * 40)
    
    # Example audio file (replace with your file)
    audio_file = "example_audio.m4a"
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file '{audio_file}' not found.")
        print("Please provide a valid audio file path.")
        return
    
    # Define methods to compare
    methods = [
        ("basic", "Basic Vosk"),
        ("enhanced", "Enhanced (0.22 model)"),
        ("ensemble", "Ensemble (multiple models)")
    ]
    
    results = {}
    
    print(f"🎵 Comparing transcription methods for: {audio_file}")
    print()
    
    # Run each method
    for method, description in methods:
        output_file = f"{method}_comparison_output.txt"
        
        print(f"🔍 Testing: {description}")
        print("-" * 30)
        
        success = run_transcription(method, audio_file, output_file)
        
        if success:
            analysis = analyze_transcription(output_file)
            if analysis:
                results[method] = {
                    'description': description,
                    'output_file': output_file,
                    'analysis': analysis
                }
                print(f"✅ {analysis['word_count']} words, Quality: {analysis['quality_score']}/100")
            else:
                print("⚠️  No transcription generated")
        else:
            print(f"❌ Failed")
        
        print()
    
    # Show comparison results
    if results:
        print("📊 COMPARISON RESULTS")
        print("=" * 50)
        
        print(f"{'Method':<25} {'Words':<8} {'Quality':<8} {'Improvements':<12}")
        print("-" * 50)
        
        best_method = None
        best_score = 0
        
        for method, data in results.items():
            analysis = data['analysis']
            print(f"{data['description']:<25} {analysis['word_count']:<8} {analysis['quality_score']:<8} {analysis['corrections_made']:<12}")
            
            if analysis['quality_score'] > best_score:
                best_score = analysis['quality_score']
                best_method = method
        
        print()
        if best_method:
            print(f"🏆 BEST RESULT: {results[best_method]['description']}")
            print(f"   Quality Score: {best_score}/100")
            print(f"   File: {results[best_method]['output_file']}")
    else:
        print("❌ No successful transcriptions to compare")

if __name__ == "__main__":
    main() 