#!/usr/bin/env python3
"""
Simple GPU Mentor App Launcher

This script provides a simple way to launch the GPU Mentor application.
"""

import sys
import os
import subprocess

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def main():
    """Main launcher function."""
    print("🚀 GPU Mentor Application Launcher")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import gradio
        print("✅ Dependencies already installed")
    except ImportError:
        print("📦 Installing dependencies...")
        if not install_requirements():
            sys.exit(1)
    
    # Check if Ollama is available
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running")
        else:
            print("⚠️ Ollama server may not be running properly")
    except:
        print("⚠️ Ollama server not detected (some features may be limited)")
    
    # Launch the app
    print("\n🌐 Starting GPU Mentor Application...")
    try:
        # Import and run the app
        from app import GPUMentorApp
        app = GPUMentorApp()
        print("🎉 Application ready! Opening in your browser...")
        app.launch(share=False)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all requirements are installed: pip install -r requirements.txt")
        print("2. Start Ollama server: ollama serve")
        print("3. Install Ollama model: ollama pull qwen2.5:14b")

if __name__ == "__main__":
    main()
