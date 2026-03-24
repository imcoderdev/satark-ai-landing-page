# 🕵️ Deepfake Detection App

Advanced AI-powered deepfake detection application using Deep Learning Model + Large Language Model (LLM) with real-time internet news scanning.

## 🌟 Features

- **🤖 Multi-Layer Detection**: Deep Learning Model + Advanced LLM analysis
- **📡 Internet Awareness**: Real-time deepfake news scanning from Google News
- **🖼️ Image Content Analysis**: Automatic description of image content
- **📊 Detailed Reports**: Comprehensive analysis with visual artifacts identification
- **📄 PDF Generation**: Legal complaint-ready PDF reports
- **🎨 Modern UI**: Beautiful interface with gradient verdict boxes and animations
- **⚖️ Risk Assessment**: Categorized risk levels (LOW, MEDIUM, HIGH)
- **🔍 Forensic Analysis**: Pixel-level manipulation detection

## 🚀 Live Demo

**[Try the app here](https://deepfake-app.streamlit.app)** *(Update after deployment)*

## 📋 Prerequisites

- Python 3.8+
- Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sanket22g/deepfake_app.git
cd deepfake_app
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API key**
   
   Create `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

4. **Run the app**
```bash
streamlit run app.py
```

## 🌐 Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `Sanket22g/deepfake_app`
6. Set main file: `app.py`
7. Add your `GEMINI_API_KEY` in the "Secrets" section
8. Click "Deploy"

### Secrets Configuration (in Streamlit Cloud):
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - Deep Learning Model API (https://deepfake-api-sn1g.onrender.com)
  - Advanced LLM (Gemini)
- **PDF Generation**: PyMuPDF (fitz)
- **News Scraping**: feedparser, BeautifulSoup4
- **Image Processing**: Pillow (PIL)

## 📦 Dependencies

```
streamlit>=1.28.0
google-generativeai>=0.3.0
Pillow>=10.0.0
PyMuPDF>=1.23.0
feedparser>=6.0.10
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 🎯 How It Works

1. **Upload Image**: User uploads an image (JPG, PNG, JPEG)
2. **Internet Scanning**: Fetches latest deepfake news trends
3. **ML Model Analysis**: Deep Learning model analyzes pixel patterns
4. **Image Description**: LLM generates content description
5. **LLM Verification**: Advanced analysis considering all factors
6. **Verdict Display**: Big colored box with REAL/FAKE verdict
7. **PDF Report**: Generate detailed forensic analysis report

## 🔒 Security

- API keys stored in Streamlit secrets
- No sensitive data committed to repository
- Secure HTTPS connections for all API calls
- XSRF protection enabled

## 📊 Analysis Features

- **Authenticity Score**: 0-100 scale
- **Confidence Level**: Detection confidence percentage
- **Risk Assessment**: LOW, MEDIUM, HIGH categorization
- **Visual Artifacts**: Facial features, lighting, texture analysis
- **Technical Issues**: Compression artifacts, pixel manipulation
- **News Context**: Current deepfake trends consideration

## 🎨 UI Features

- Gradient verdict boxes (Red for FAKE, Green for REAL)
- Balloon animation for authentic images
- Internet news sidebar
- Threat intelligence dashboard
- Mobile-responsive design

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Sanket Ghodke**
- GitHub: [@Sanket22g](https://github.com/Sanket22g)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Always verify results with multiple sources. The AI analysis should not be considered as definitive legal evidence without further forensic verification.

## 📧 Support

For issues and questions, please [open an issue](https://github.com/Sanket22g/deepfake_app/issues) on GitHub.

---

⭐ **Star this repo if you find it useful!**

🔗 **Share with others to spread awareness about deepfakes!**
