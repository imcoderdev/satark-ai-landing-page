"""
Wrapper for Deepfake Detection module
"""
import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

def run_deepfake_app():
    """Execute the Deepfake Detection application"""
    try:
        # Get the path to deepfakeapp directory
        current_dir = Path(__file__).parent
        deepfake_dir = current_dir / "deepfakeapp"

        # Load environment variables from root .env file
        root_env_path = current_dir / ".env"
        if root_env_path.exists():
            load_dotenv(root_env_path)

        # Save current working directory
        original_cwd = os.getcwd()

        # Change to deepfakeapp directory
        os.chdir(deepfake_dir)

        # Add to Python path
        if str(deepfake_dir) not in sys.path:
            sys.path.insert(0, str(deepfake_dir))

        # Import and run the main function
        from app import main as deepfake_main

        # Run the deepfake app
        deepfake_main()

    except Exception as e:
        st.error(f"❌ Error loading Deepfake App: {str(e)}")
        st.info("Please check if all dependencies are installed and the deepfakeapp module exists.")
        st.info("Make sure to configure your .env file with the required API keys.")

    finally:
        # Restore original working directory
        try:
            os.chdir(original_cwd)
        except:
            pass