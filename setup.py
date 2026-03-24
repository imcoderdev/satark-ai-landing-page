#!/usr/bin/env python3
"""
Satark AI - Quick Setup Script
Automates the initial setup process for the Satark AI application
"""
import os
import sys
import shutil
from pathlib import Path

def main():
    """Main setup function"""
    print("Satark AI - Quick Setup")
    print("=" * 40)

    current_dir = Path(__file__).parent

    # Check if .env.example exists
    env_example = current_dir / ".env.example"
    env_file = current_dir / ".env"

    if not env_example.exists():
        print("[ERROR] .env.example file not found!")
        return False

    # Copy .env.example to .env if it doesn't exist
    if not env_file.exists():
        shutil.copy2(env_example, env_file)
        print("[OK] Created .env file from template")
    else:
        print("[INFO] .env file already exists, skipping copy")

    # Check if required directories exist
    satark_dir = current_dir / "satark-ai"
    deepfake_dir = current_dir / "deepfakeapp"

    if not satark_dir.exists():
        print("[ERROR] satark-ai directory not found!")
        return False

    if not deepfake_dir.exists():
        print("[ERROR] deepfakeapp directory not found!")
        return False

    print("[OK] Application directories found")

    # Check if app files exist
    satark_app = satark_dir / "app.py"
    deepfake_app = deepfake_dir / "app.py"

    if not satark_app.exists():
        print("[ERROR] satark-ai/app.py not found!")
        return False

    if not deepfake_app.exists():
        print("[ERROR] deepfakeapp/app.py not found!")
        return False

    print("[OK] Application files found")

    # Check if requirements.txt exists
    requirements_file = current_dir / "requirements.txt"
    if not requirements_file.exists():
        print("[ERROR] requirements.txt not found!")
        return False

    print("[OK] Requirements file found")

    # Installation instructions
    print("\nNext Steps:")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Configure your .env file:")
    print(f"   Edit: {env_file}")
    print("   - Add your Gemini API key")
    print("   - Add Gmail credentials (optional)")
    print("\n3. Get API keys:")
    print("   - Gemini API: https://makersuite.google.com/app/apikey")
    print("   - Gmail App Password: https://myaccount.google.com/apppasswords")
    print("\n4. Run the application:")
    print("   streamlit run main.py")

    print("\nSetup complete! Follow the next steps to get started.")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        sys.exit(1)