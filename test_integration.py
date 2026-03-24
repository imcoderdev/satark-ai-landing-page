"""
Test script to verify the landing page integration
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    try:
        import streamlit
        print("[OK] Streamlit imported successfully")
    except ImportError as e:
        print(f"[ERROR] Streamlit import failed: {e}")
        return False

    try:
        from satark_wrapper import run_satark_ai
        print("[OK] Satark AI wrapper imported successfully")
    except ImportError as e:
        print(f"[ERROR] Satark wrapper import failed: {e}")

    try:
        from deepfake_wrapper import run_deepfake_app
        print("[OK] Deepfake wrapper imported successfully")
    except ImportError as e:
        print(f"[ERROR] Deepfake wrapper import failed: {e}")

    return True

def test_app_structure():
    """Test if the required app files exist"""
    print("\nTesting app structure...")

    current_dir = Path(__file__).parent
    satark_ai_app = current_dir / "satark-ai" / "app.py"
    deepfake_app = current_dir / "deepfakeapp" / "app.py"

    if satark_ai_app.exists():
        print("[OK] Satark AI app.py found")
    else:
        print("[ERROR] Satark AI app.py not found")

    if deepfake_app.exists():
        print("[OK] Deepfake app.py found")
    else:
        print("[ERROR] Deepfake app.py not found")

    return True

def main():
    """Run all tests"""
    print("Satark AI Landing Page - Test Suite\n")

    test_imports()
    test_app_structure()

    print("\nTesting complete!")
    print("\nTo run the landing page:")
    print("streamlit run main.py")

if __name__ == "__main__":
    main()