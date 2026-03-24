"""
🛡️ Satark AI - Landing Page
Your AI Safety Bodyguard
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Import wrappers for the individual apps
from satark_wrapper import run_satark_ai
from deepfake_wrapper import run_deepfake_app

def set_dark_theme():
    """Configure dark theme and custom styling"""
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 3rem;
        }

        .main-title {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #ffffff;
        }

        .main-subtitle {
            font-size: 1.2rem;
            color: #cccccc;
            margin-bottom: 2rem;
        }

        .app-card {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }

        .app-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }

        .app-card-title {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #ffffff;
        }

        .app-card-desc {
            font-size: 1rem;
            color: #e0e0e0;
            margin-bottom: 2rem;
            line-height: 1.6;
        }

        .stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1rem;
            width: 100%;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(45deg, #764ba2, #667eea);
            transform: scale(1.05);
        }

        .back-button {
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 999;
        }

        .back-button button {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }

        /* Dark theme override */
        .stApp {
            background: linear-gradient(135deg, #0c0c0c, #1a1a2e, #16213e);
            color: white;
        }

        .stMarkdown {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

def show_landing_page():
    """Display the main landing page"""

    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🛡️ Satark AI</h1>
        <p class="main-subtitle">"Your AI Safety Bodyguard"</p>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns for the cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="app-card">
            <h2 class="app-card-title">🛡️ Satark AI</h2>
            <p class="app-card-desc">
                Detect scams from WhatsApp/SMS screenshots using advanced AI analysis.
                Protect yourself from financial fraud and cyber threats.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Satark AI", key="satark_btn", use_container_width=True):
            st.session_state.page = "satark"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="app-card">
            <h2 class="app-card-title">🎭 Deepfake App</h2>
            <p class="app-card-desc">
                Detect fake or manipulated images using cutting-edge AI technology.
                Verify the authenticity of visual content.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Deepfake Detector", key="deepfake_btn", use_container_width=True):
            st.session_state.page = "deepfake"
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #888;'>
        <p style='margin-bottom: 0.5rem;'>🛡️ Protecting you with AI-powered security solutions</p>
        <p style='font-size: 0.8rem;'>Made with ❤️ by Team Tark | © 2025 Satark AI</p>
    </div>
    """, unsafe_allow_html=True)

def start_satark_ai():
    """Launch the Satark AI module"""
    # Add back button
    show_back_button()

    # Run the Satark AI app
    run_satark_ai()

def start_deepfake_app():
    """Launch the Deepfake Detection module"""
    # Add back button
    show_back_button()

    # Run the Deepfake app
    run_deepfake_app()

def show_back_button():
    """Display back button to return to landing page"""
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_btn"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application logic"""

    # Configure page
    st.set_page_config(
        page_title="🛡️ Satark AI - Your AI Safety Bodyguard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply dark theme
    set_dark_theme()

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"

    # Navigation logic
    if st.session_state.page == "home":
        show_landing_page()

    elif st.session_state.page == "satark":
        start_satark_ai()

    elif st.session_state.page == "deepfake":
        start_deepfake_app()

    else:
        # Fallback to home page
        st.session_state.page = "home"
        st.rerun()

if __name__ == "__main__":
    main()