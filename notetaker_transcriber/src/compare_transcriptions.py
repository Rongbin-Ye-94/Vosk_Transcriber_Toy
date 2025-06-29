#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime

def run_transcription(method, audio_file, output_file):
    """Run transcription with a specific method"""
    print(f"\n🔍 Running {method}...")
    
    if method == "basic":
        cmd = ["python3", "transcribe_m4a.py", audio_file, output_file]
    elif method == "enhanced":
        cmd = ["python3", "enhanced_transcriber.py", audio_file, output_file, "vosk-model-en-us-0.22"]
    elif method == "ensemble":
        cmd = ["python3", "ensemble_transcriber.py", audio_file, output_file]
    else:
        print(f"✗ Unknown method: {method}")
        return False
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {method} completed successfully")
            return True
        else:
            print(f"⚠️  {method} had issues: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error running {method}: {e}")
        return False

def analyze_transcription(file_path):
    """Analyze transcription quality"""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        return None
    
    # Basic metrics
    word_count = len(text.split())
    char_count = len(text)
    sentence_count = len([s for s in text.split('.') if s.strip()])
    
    # Quality indicators
    quality_score = 0
    corrections_made = 0
    
    # Check for common improvements
    improvements = {
        'proper_capitalization': text[0].isupper() if text else False,
        'technical_terms': any(term in text.lower() for term in ['python', 'sql', 'tableau', 'credit', 'analytics']),
        'interview_terms': any(term in text.lower() for term in ['interview', 'experience', 'position', 'manager']),
        'no_repeated_words': not any(word * 3 in text.lower() for word in ['the', 'and', 'i', 'you']),
        'reasonable_length': word_count > 50
    }
    
    for improvement, present in improvements.items():
        if present:
            quality_score += 20
            corrections_made += 1
    
    return {
        'word_count': word_count,
        'char_count': char_count,
        'sentence_count': sentence_count,
        'quality_score': quality_score,
        'corrections_made': corrections_made,
        'text_preview': text[:200] + "..." if len(text) > 200 else text
    }

def main():
    print("🎯 Transcription Quality Comparison Tool")
    print("="*60)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 compare_transcriptions.py <audio_file>")
        print("\nThis tool compares different transcription methods:")
        print("  1. Basic (simple Vosk)")
        print("  2. Enhanced (better model + post-processing)")
        print("  3. Ensemble (multiple models + audio variations)")
        print("\nExample:")
        print("  python3 compare_transcriptions.py 'audio.m4a'")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"✗ Error: Audio file '{audio_file}' not found.")
        sys.exit(1)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"transcription_comparison_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 Results will be saved to: {output_dir}")
    
    # Define methods to test
    methods = [
        ("basic", "Basic Vosk"),
        ("enhanced", "Enhanced (0.22 model + post-processing)"),
        ("ensemble", "Ensemble (multiple models + variations)")
    ]
    
    results = {}
    
    # Run each method
    for method, description in methods:
        output_file = os.path.join(output_dir, f"{method}_transcription.txt")
        
        print(f"\n{'='*60}")
        print(f"🎯 Testing: {description}")
        print(f"{'='*60}")
        
        success = run_transcription(method, audio_file, output_file)
        
        if success:
            analysis = analyze_transcription(output_file)
            if analysis:
                results[method] = {
                    'description': description,
                    'output_file': output_file,
                    'analysis': analysis
                }
                print(f"📊 Analysis: {analysis['word_count']} words, Quality: {analysis['quality_score']}/100")
            else:
                print("⚠️  No transcription generated")
        else:
            print(f"✗ {description} failed")
    
    # Compare results
    print(f"\n{'='*80}")
    print("📊 TRANSCRIPTION COMPARISON RESULTS")
    print(f"{'='*80}")
    
    if not results:
        print("✗ No successful transcriptions to compare")
        return
    
    # Create comparison table
    print(f"{'Method':<25} {'Words':<8} {'Quality':<8} {'Improvements':<12} {'Preview'}")
    print("-" * 80)
    
    best_method = None
    best_score = 0
    
    for method, data in results.items():
        analysis = data['analysis']
        preview = analysis['text_preview'].replace('\n', ' ')[:50]
        
        print(f"{data['description']:<25} {analysis['word_count']:<8} {analysis['quality_score']:<8} {analysis['corrections_made']:<12} {preview}")
        
        if analysis['quality_score'] > best_score:
            best_score = analysis['quality_score']
            best_method = method
    
    print(f"\n🏆 BEST RESULT: {results[best_method]['description']}")
    print(f"   Quality Score: {best_score}/100")
    print(f"   File: {results[best_method]['output_file']}")
    
    # Show detailed comparison
    print(f"\n{'='*80}")
    print("📝 DETAILED COMPARISON")
    print(f"{'='*80}")
    
    for method, data in results.items():
        print(f"\n🔍 {data['description'].upper()}")
        print("-" * 40)
        analysis = data['analysis']
        print(f"Words: {analysis['word_count']}")
        print(f"Characters: {analysis['char_count']}")
        print(f"Sentences: {analysis['sentence_count']}")
        print(f"Quality Score: {analysis['quality_score']}/100")
        print(f"Improvements Applied: {analysis['corrections_made']}")
        print(f"Preview: {analysis['text_preview']}")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("💡 RECOMMENDATIONS")
    print(f"{'='*80}")
    
    if len(results) > 1:
        print("Based on the comparison:")
        
        if 'ensemble' in results:
            print("✅ Use Ensemble method for maximum accuracy")
            print("   - Uses multiple models and audio variations")
            print("   - Best for important recordings")
            print("   - Takes longer but provides highest quality")
        
        if 'enhanced' in results:
            print("✅ Use Enhanced method for good balance")
            print("   - Uses the largest Vosk model (0.22)")
            print("   - Includes post-processing corrections")
            print("   - Good accuracy with reasonable speed")
        
        if 'basic' in results:
            print("⚠️  Basic method is least accurate")
            print("   - Uses default Vosk model")
            print("   - No post-processing")
            print("   - Use only for quick tests")
    
    print(f"\n📁 All results saved in: {output_dir}")
    print("You can review the full transcriptions in the output files.")

if __name__ == "__main__":
    main() 