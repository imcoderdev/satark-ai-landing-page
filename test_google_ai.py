#!/usr/bin/env python3
"""
Test Google Generative AI import and configuration
"""
import os
import sys
from pathlib import Path

def test_google_ai_import():
    """Test if Google Generative AI can be imported and configured"""
    print("Testing Google Generative AI setup...")

    try:
        import google.generativeai as genai
        print("[OK] Google Generative AI imported successfully")

        # Test configuration with dummy key
        genai.configure(api_key="test_key")
        print("[OK] genai.configure() works properly")

        # Test model creation (will fail without real key, but should not crash)
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("[OK] GenerativeModel creation works")
        except Exception as e:
            if "API" in str(e) or "key" in str(e):
                print("[OK] Model creation requires valid API key (expected)")
            else:
                print(f"[WARNING] Unexpected model creation error: {e}")

        return True

    except ImportError as e:
        print(f"[ERROR] Failed to import Google Generative AI: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def main():
    """Run Google AI tests"""
    print("Google Generative AI Test Suite")
    print("=" * 35)

    success = test_google_ai_import()

    if success:
        print("\n[OK] All tests passed! Google Generative AI is properly configured.")
        print("\nTo use the apps:")
        print("1. Set your GEMINI_API_KEY in the .env file")
        print("2. Run: streamlit run main.py")
    else:
        print("\n[ERROR] Google Generative AI setup failed!")
        print("Try: pip install --upgrade google-generativeai")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)