"""
Wrapper for Satark AI module
"""
import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

def run_satark_ai():
    """Execute the Satark AI application"""
    try:
        # Get the path to satark-ai directory
        current_dir = Path(__file__).parent
        satark_ai_dir = current_dir / "satark-ai"

        # Load environment variables from root .env file
        root_env_path = current_dir / ".env"
        if root_env_path.exists():
            load_dotenv(root_env_path)

        # Save current working directory
        original_cwd = os.getcwd()

        # Change to satark-ai directory
        os.chdir(satark_ai_dir)

        # Add to Python path
        if str(satark_ai_dir) not in sys.path:
            sys.path.insert(0, str(satark_ai_dir))

        # Import and execute the app
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "satark_app",
            satark_ai_dir / "app.py"
        )
        satark_module = importlib.util.module_from_spec(spec)

        # Execute the module (this will run the Streamlit code)
        spec.loader.exec_module(satark_module)

    except Exception as e:
        st.error(f"❌ Error loading Satark AI: {str(e)}")
        st.info("Please check if all dependencies are installed and the satark-ai module exists.")
        st.info("Make sure to configure your .env file with the required API keys.")

    finally:
        # Restore original working directory
        try:
            os.chdir(original_cwd)
        except:
            pass