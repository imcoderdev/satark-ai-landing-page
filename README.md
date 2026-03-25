# 🛡️ Satark AI - Landing Page

Your AI Safety Bodyguard - A unified interface for scam detection and deepfake detection applications.

## Features

- **🛡️ Satark AI**: Detect scams from WhatsApp/SMS screenshots
- **🎭 Deepfake App**: Detect fake or manipulated images
- **Dark Theme**: Modern, user-friendly interface
- **Easy Navigation**: Session-based navigation between apps
- **Unified Configuration**: Single .env file for both applications

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual API keys
# Get Gemini API key from: https://makersuite.google.com/app/apikey
```

3. Ensure both applications exist in their respective directories:
   - `satark-ai/app.py`
   - `deepfakeapp/app.py`

## Configuration

### 🔑 Required Environment Variables

The application uses a unified `.env` file in the root directory:

```env
# Google Gemini AI API Key (Required for both apps)
GEMINI_API_KEY=your_gemini_api_key_here

# Gmail Configuration (Optional - for Satark AI email alerts)
GMAIL_SENDER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password_here
```

### 🔐 Security Notes

- **Never commit `.env` file** to version control
- **Use App Passwords** for Gmail (not regular password)
- **Keep API keys secure** and rotate them regularly
- **Use `.env.example`** as a template for new setups

## Deployment

### Streamlit Cloud Deployment

To deploy on Streamlit Cloud:

1. **Fork or use this repository**: [https://github.com/imcoderdev/satark-ai-landing-page](https://github.com/imcoderdev/satark-ai-landing-page)

2. **Configure secrets** in Streamlit Cloud dashboard:
   ```toml
   # Add in app settings -> Secrets
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   GMAIL_SENDER = "your_email@gmail.com"  # Optional
   GMAIL_APP_PASSWORD = "your_app_password"  # Optional
   ```

3. **Set main file path**: `main.py`

4. **Dependencies**: All requirements are automatically installed from `requirements.txt`

### Local Development

1. Clone and setup:
   ```bash
   git clone https://github.com/imcoderdev/satark-ai-landing-page.git
   cd satark-ai-landing-page
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Test dependencies (optional):
   ```bash
   python test_dependencies.py
   ```

4. Run the app:
   ```bash
   streamlit run main.py
   ```

## Project Structure

```
.
├── main.py                 # Main landing page application
├── satark_wrapper.py       # Wrapper for Satark AI module
├── deepfake_wrapper.py     # Wrapper for Deepfake module
├── .env                    # Environment configuration (create from .env.example)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── satark-ai/
│   └── app.py             # Satark AI scam detection app
└── deepfakeapp/
    └── app.py             # Deepfake detection app
```

## Navigation

- **Home**: Landing page with app selection
- **Back Button**: Available in each app to return to home
- **Session State**: Maintains navigation state across interactions

## Environment Setup Guide

### 1. Google Gemini AI API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### 2. Gmail Configuration (Optional)
For Satark AI email alerts:
1. Enable 2-factor authentication on Gmail
2. Generate App Password at [Google Account](https://myaccount.google.com/apppasswords)
3. Add your email and app password to `.env`

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Import Errors**: Check if all dependencies are installed
3. **Email Not Working**: Verify Gmail App Password setup
4. **Apps Not Loading**: Ensure `satark-ai/app.py` and `deepfakeapp/app.py` exist

### Known Issues

- **Google Generative AI Deprecation Warning**: The `google.generativeai` package is being deprecated in favor of `google.genai`. This doesn't affect functionality but may show warnings. Consider updating to the new package in future versions.

### Recent Fixes (March 2025)

- ✅ **Fixed missing dependencies**: Added `duckduckgo-search`, `fpdf2`, `pymupdf`, `feedparser`
- ✅ **Fixed Google AI import**: Updated from deprecated `genai.Client()` to `genai.GenerativeModel()`
- ✅ **Fixed encoding issues**: Clean UTF-8 requirements.txt for deployment compatibility
- ✅ **Added dependency testing**: `test_dependencies.py` script for troubleshooting

### Testing Setup

Run the integration test:
```bash
python test_integration.py
```

Test Google AI configuration:
```bash
python test_google_ai.py
```

This will verify:
- All required imports work
- Both app files exist
- Environment configuration is accessible
- Google Generative AI is properly configured

---

Made with ❤️ by Team Tark | © 2025 Satark AI