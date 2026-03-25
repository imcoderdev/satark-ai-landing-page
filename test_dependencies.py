#!/usr/bin/env python3
"""
Test all dependencies for Satark AI Landing Page
Verifies that all required packages can be imported successfully
"""
import sys

def test_core_dependencies():
    """Test core framework dependencies"""
    print("Testing core dependencies...")

    try:
        import streamlit as st
        print("[OK] streamlit")
    except ImportError as e:
        print(f"[ERROR] streamlit: {e}")
        return False

    try:
        from PIL import Image
        print("[OK] pillow (PIL)")
    except ImportError as e:
        print(f"[ERROR] pillow: {e}")
        return False

    try:
        from dotenv import load_dotenv
        print("[OK] python-dotenv")
    except ImportError as e:
        print(f"[ERROR] python-dotenv: {e}")
        return False

    return True

def test_ai_dependencies():
    """Test AI and ML dependencies"""
    print("\nTesting AI dependencies...")

    try:
        import google.generativeai as genai
        print("[OK] google-generativeai")
    except ImportError as e:
        print(f"[ERROR] google-generativeai: {e}")
        return False

    return True

def test_satark_ai_dependencies():
    """Test Satark AI specific dependencies"""
    print("\nTesting Satark AI dependencies...")

    try:
        from duckduckgo_search import DDGS
        print("[OK] duckduckgo-search")
    except ImportError as e:
        print(f"[ERROR] duckduckgo-search: {e}")
        return False

    try:
        from fpdf import FPDF
        print("[OK] fpdf2")
    except ImportError as e:
        print(f"[ERROR] fpdf2: {e}")
        return False

    try:
        from bs4 import BeautifulSoup
        print("[OK] beautifulsoup4")
    except ImportError as e:
        print(f"[ERROR] beautifulsoup4: {e}")
        return False

    try:
        import requests
        print("[OK] requests")
    except ImportError as e:
        print(f"[ERROR] requests: {e}")
        return False

    return True

def test_deepfake_dependencies():
    """Test Deepfake app specific dependencies"""
    print("\nTesting Deepfake app dependencies...")

    try:
        import fitz  # PyMuPDF
        print("[OK] pymupdf (fitz)")
    except ImportError as e:
        print(f"[ERROR] pymupdf: {e}")
        return False

    try:
        import feedparser
        print("[OK] feedparser")
    except ImportError as e:
        print(f"[ERROR] feedparser: {e}")
        return False

    return True

def main():
    """Run all dependency tests"""
    print("Satark AI - Dependency Test Suite")
    print("=" * 40)

    tests = [
        test_core_dependencies,
        test_ai_dependencies,
        test_satark_ai_dependencies,
        test_deepfake_dependencies
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "=" * 40)
    if all_passed:
        print("[SUCCESS] All dependencies are available!")
        print("[OK] The application should run without import errors.")
    else:
        print("[ERROR] Some dependencies are missing!")
        print("[FIX] Run: pip install -r requirements.txt")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)