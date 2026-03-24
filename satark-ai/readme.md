SYSTEM: ACT AS SENIOR HACKATHON ENGINEER
PROJECT: "SATARK.AI" (Team Tark)
EVENT: ML Nashik Gen AI-thon 2025
DEADLINE: 12 HOURS. SPEED IS PRIORITY.

---

### 🚀 THE MISSION
We are building "Satark.ai" — an Autonomous AI Agent that acts as a financial bodyguard for Indian users (Tier-2/3 cities).
The Problem: People get scammed by predatory loan apps, fake lottery messages, and "Digital Arrest" threats.
The Solution: A web app where users upload a screenshot (WhatsApp/SMS), and the Agent analyzes it to detect scams using Multimodal AI.

---

### 🛠️ THE TECH STACK
1.  **Language:** Python 3.9+
2.  **Frontend:** Streamlit (Must look clean and "Trustworthy").
3.  **AI Model:** Google Gemini 1.5 Flash (via `google-generativeai` library).
4.  **Capabilities:** Computer Vision (to read screenshots) + Reasoning (to find red flags).

---

### 🧠 THE AGENT LOGIC (THE "SECRET SAUCE")
The agent must follow this "Chain of Thought" for every image:
1.  **OCR & Extraction:** Read the text. Identify Company Name, Amount, Phone Number.
2.  **Rule Checking (Simulated Tools):**
    * *Check 1:* Is the language threatening? (Urgency = High Risk)
    * *Check 2:* Does it ask for upfront fees? (Fees = Scam)
    * *Check 3:* Is the grammar broken? (Typos = Suspicious)
3.  **The "Fake" Database Search (Hackathon Trick):**
    * If the text contains specific keywords (e.g., "Laxmi Chit Fund", "RbiApproved_Loan_apk"), the Agent must simulate a database lookup and return "BLACKLISTED ENTITY FOUND".
4.  **Final Output:**
    * **Verdict:** SAFE / SUSPICIOUS / SCAM.
    * **Action:** "Block this number immediately" / "Delete this app".
    * **Tone:** "Desi Big Brother" (Hinglish, protective, slightly savage).

---

### 📂 PROJECT STRUCTURE
We will keep it simple. Guide me to build these files:
1.  `app.py`: The main Streamlit application.
2.  `requirements.txt`: The dependencies.
3.  `prompts.py`: Storing the system prompts separately (clean code).

---

### 🎯 YOUR INSTRUCTIONS
1.  **Do not** give me generic advice. Give me code.
2.  **Do not** worry about security or best practices. We need it to run *now*.
3.  **Start by giving me the folder structure and the `requirements.txt` file.**
4.  **Then, write the `app.py` code step-by-step.**

I am ready. Let's build Satark.ai.