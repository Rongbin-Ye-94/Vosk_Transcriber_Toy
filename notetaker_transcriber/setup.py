#!/usr/bin/env python3
"""
Setup script for Notetaker Transcriber
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="notetaker-transcriber",
    version="1.0.0",
    author="Notetaker Transcriber Team",
    author_email="contact@notetaker-transcriber.com",
    description="A powerful, offline speech-to-text transcription system with voice adaptation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/notetaker_transcriber",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ],
        "training": [
            "torch>=1.12.0",
            "torchaudio>=0.12.0",
            "librosa>=0.9.0",
            "soundfile>=0.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "notetaker-transcribe=src.transcribe_m4a:main",
            "notetaker-enhanced=src.enhanced_transcriber:main",
            "notetaker-ensemble=src.ensemble_transcriber:main",
            "notetaker-custom=src.custom_training_transcriber:main",
            "notetaker-compare=src.compare_transcriptions:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords="speech recognition transcription vosk offline voice adaptation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/notetaker_transcriber/issues",
        "Source": "https://github.com/yourusername/notetaker_transcriber",
        "Documentation": "https://github.com/yourusername/notetaker_transcriber/docs",
    },
) 