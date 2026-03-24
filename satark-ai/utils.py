"""
Satark.ai - Utility Functions
Google Gemini API Integration
"""

import google.generativeai as genai
from PIL import Image
import json
import os
import re
import time
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from live_scraper import live_db, check_phone, check_upi


load_dotenv()


DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY")


SCAM_DETECTION_PROMPT = """You are "Satark.ai" - a financial scam detection AI agent acting as a protective "Desi Big Brother" for Indian users.

Analyze this screenshot (WhatsApp/SMS/App) and detect if it's a financial scam.

## Your Analysis Process:
1. **OCR & Extract:** Read all visible text. Identify: Company Name, Phone Numbers, Amounts, URLs, App Names.
2. **Check Red Flags:**
   - Threatening/urgent language ("Pay now or jail", "Digital Arrest", "Last warning")
   - Requests for upfront fees before loan disbursement
   - Unrealistic promises (lottery wins, guaranteed returns >15%)
   - Poor grammar/spelling mistakes
   - Requests for OTP, UPI PIN, or bank details
   - Unknown/suspicious sender numbers
   - Fake government/bank impersonation (RBI, SBI, CBI, Police)
3. **Blacklist Check:** Flag keywords like "Laxmi Chit Fund", "RbiApproved_Loan", "Digital Arrest", "Cyber Cell Arrest", "Lottery Winner" as SCAM.

## STRICT JSON OUTPUT FORMAT (NO OTHER TEXT):
{
    "verdict": "SCAM" | "SUSPICIOUS" | "SAFE",
    "risk_score": <0-100 integer>,
    "scam_type": "<e.g., Lottery Scam, Phishing, Loan Fraud, Digital Arrest, UPI Fraud, or 'None' if safe>",
    "extracted_entities": {
        "company_name": "<extracted or null>",
        "phone_number": "<extracted or null>",
        "amount": "<extracted or null>",
        "upi_id": "<extracted or null>",
        "url": "<extracted or null>"
    },
    "red_flags": ["<flag1>", "<flag2>"],
    "reasoning": "<Technical 2-3 sentence explanation of why this is a scam/safe>",
    "hinglish_advice": "<Safety advice in the language specified below>"
}

IMPORTANT: Respond with ONLY valid JSON. No markdown code blocks. No extra text before or after."""


# Language-specific prompt additions
LANGUAGE_INSTRUCTIONS = {
    "Hinglish": """
LANGUAGE INSTRUCTION: Provide the 'reasoning' and 'hinglish_advice' fields in HINGLISH (Hindi-English mix).
Use a savage, protective Gen-Z style. Be dramatic and use phrases like:
- "Bhaag ja bhai!"
- "Yeh 100% fraud hai!"
- "Paise bachao, isko block karo!"
- "Red flag spotted! Danger zone mein ho tum!"
""",
    "English": """
LANGUAGE INSTRUCTION: Provide the 'reasoning' and 'hinglish_advice' fields in FORMAL ENGLISH.
Use a professional, clear tone. Be direct and informative.
""",
    "Hindi": """
LANGUAGE INSTRUCTION: Provide the 'reasoning' and 'hinglish_advice' fields in PURE HINDI (Devanagari script).
Use a protective, caring tone like a concerned elder brother. Examples:
- "सावधान रहो भाई!"
- "यह धोखाधड़ी है!"
- "तुरंत ब्लॉक करो!"
- "पुलिस में शिकायत करो!"
""",
    "Marathi": """
LANGUAGE INSTRUCTION: Provide the 'reasoning' and 'hinglish_advice' fields in MARATHI (Devanagari script).
Use a stern, authoritative tone like a strict elder. Examples:
- "सावध रहा!"
- "हे फसवणूक आहे!"
- "लगेच ब्लॉक करा!"
- "सायबर सेलला तक्रार करा!"
"""
}


def get_prompt_with_language(language: str) -> str:
    """Get the scam detection prompt with language-specific instructions."""
    base_prompt = SCAM_DETECTION_PROMPT
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS["Hinglish"])
    return f"{base_prompt}\n\n{lang_instruction}"


def configure_gemini(api_key: str):
    """Configure the Gemini API with the provided key."""
    genai.configure(api_key=api_key)


def analyze_screenshot(image: Image.Image, api_key: str = None, language: str = "Hinglish") -> dict:
    """
    Analyze a screenshot for potential scams using Gemini 2.5 Flash.
    
    Args:
        image: PIL Image object of the screenshot
        api_key: Google Gemini API key (optional, uses default if not provided)
    
    Returns:
        dict with verdict, risk_score, reasoning, and all analysis data
    """
    # Use provided key or fallback to default from environment
    key = api_key or DEFAULT_API_KEY
    if not key:
        return {
            "verdict": "ERROR",
            "risk_score": 0,
            "scam_type": "N/A",
            "extracted_entities": {},
            "red_flags": [],
            "reasoning": "Gemini API key missing. Set GEMINI_API_KEY in your environment or .env file.",
            "hinglish_advice": "API key daal pehle bhai!",
            "latency_ms": 0,
            "raw_response": None,
            "parse_success": False
        }
    
    configure_gemini(key)
    
    # Start timing
    start_time = time.time()
    
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Get language-specific prompt
        prompt = get_prompt_with_language(language)
        
        # Send image with prompt to Gemini
        response = model.generate_content([prompt, image])
        
        # Calculate latency
        end_time = time.time()
        latency_ms = round((end_time - start_time) * 1000, 2)
        
        # Get raw response text
        response_text = response.text.strip()
        raw_response = response_text  # Store original for debug
        
        # Clean up response if it has markdown code blocks
        if response_text.startswith("```"):
            response_text = re.sub(r'^```json?\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
        
        # Parse JSON
        result = json.loads(response_text)
        
        # Ensure all required keys exist with defaults
        result.setdefault("verdict", "SUSPICIOUS")
        result.setdefault("risk_score", 50)
        result.setdefault("scam_type", "Unknown")
        result.setdefault("extracted_entities", {})
        result.setdefault("red_flags", [])
        result.setdefault("reasoning", "Analysis complete.")
        result.setdefault("hinglish_advice", "Sambhal ke reh bhai!")
        
        # Add metadata
        result["latency_ms"] = latency_ms
        result["raw_response"] = raw_response
        result["parse_success"] = True
        result["model"] = "gemini-2.5-flash"
        
        # Legacy compatibility
        result["extracted_info"] = result.get("extracted_entities", {})
        result["action"] = result.get("hinglish_advice", "Stay alert!")
        result["blacklisted_entity"] = result.get("scam_type", "").lower() in ["ponzi scheme", "blacklisted", "known scam"]
        
        return result
        
    except json.JSONDecodeError as e:
        end_time = time.time()
        latency_ms = round((end_time - start_time) * 1000, 2)
        
        return {
            "verdict": "SUSPICIOUS",
            "risk_score": 50,
            "scam_type": "Parse Error",
            "extracted_entities": {},
            "red_flags": ["JSON parsing failed"],
            "reasoning": f"Could not parse AI response. Raw output available in debug mode.",
            "hinglish_advice": "Bhai, kuch technical issue hai. But sambhal ke reh!",
            "latency_ms": latency_ms,
            "raw_response": response.text if 'response' in locals() else str(e),
            "parse_success": False,
            "model": "gemini-2.5-flash",
            "extracted_info": {},
            "action": "Try again or manually review.",
            "blacklisted_entity": False
        }
        
    except Exception as e:
        end_time = time.time()
        latency_ms = round((end_time - start_time) * 1000, 2) if 'start_time' in locals() else 0
        
        return {
            "verdict": "ERROR",
            "risk_score": 0,
            "scam_type": "API Error",
            "extracted_entities": {},
            "red_flags": [str(e)],
            "reasoning": f"API Error: {str(e)}",
            "hinglish_advice": "API mein dikkat hai, baad mein try kar.",
            "latency_ms": latency_ms,
            "raw_response": str(e),
            "parse_success": False,
            "model": "gemini-2.5-flash",
            "extracted_info": {},
            "action": "Check your API key and try again.",
            "blacklisted_entity": False
        }


# Simulated blacklist database (Hackathon trick)
BLACKLISTED_KEYWORDS = [
    "laxmi chit fund",
    "rbiapproved_loan",
    "instant loan apk",
    "digital arrest",
    "cyber cell arrest",
    "pay now or jail",
    "lottery winner",
    "nigeria prince",
    "send otp",
    "share otp"
]


# Scam Database - Fake scam apps vs Real banks
SCAM_DATABASE = {
    # Fake Indian Scam Apps (10)
    "scam_apps": [
        {"name": "Laxmi Chit Fund", "type": "Ponzi Scheme", "risk": 100},
        {"name": "EasyLoan 24x7", "type": "Predatory Loan App", "risk": 95},
        {"name": "RBI Approved Loan APK", "type": "Fake RBI Impersonation", "risk": 100},
        {"name": "Shree Ganesh Finance", "type": "Illegal NBFC", "risk": 90},
        {"name": "QuickCash India", "type": "Predatory Loan App", "risk": 95},
        {"name": "Bharat Money Lender", "type": "Harassment App", "risk": 92},
        {"name": "Golden Harvest Scheme", "type": "Ponzi Scheme", "risk": 100},
        {"name": "InstaCred Pro", "type": "Data Theft App", "risk": 88},
        {"name": "PM Yojana Loan", "type": "Govt Impersonation", "risk": 100},
        {"name": "SBI Direct Loan WhatsApp", "type": "Bank Impersonation", "risk": 98},
    ],
    # Real Legitimate Banks (5)
    "real_banks": [
        {"name": "State Bank of India", "type": "PSU Bank", "risk": 0},
        {"name": "HDFC Bank", "type": "Private Bank", "risk": 0},
        {"name": "ICICI Bank", "type": "Private Bank", "risk": 0},
        {"name": "Axis Bank", "type": "Private Bank", "risk": 0},
        {"name": "Punjab National Bank", "type": "PSU Bank", "risk": 0},
    ]
}


def check_database(name: str) -> dict:
    """
    Fuzzy match input text against SCAM_DATABASE.
    
    Args:
        name: Company/app name to check
    
    Returns:
        dict with match_found, entity_type, entity_name, risk_score, is_scam
    """
    if not name:
        return {"match_found": False, "is_scam": False}
    
    name_lower = name.lower().strip()
    
    # Check scam apps first (higher priority)
    for scam in SCAM_DATABASE["scam_apps"]:
        scam_name_lower = scam["name"].lower()
        
        # Fuzzy matching: check if significant words match
        scam_words = set(scam_name_lower.split())
        input_words = set(name_lower.split())
        
        # Direct substring match
        if scam_name_lower in name_lower or name_lower in scam_name_lower:
            return {
                "match_found": True,
                "entity_type": scam["type"],
                "entity_name": scam["name"],
                "risk_score": scam["risk"],
                "is_scam": True,
                "message": f"🚨 BLACKLISTED: {scam['name']} - {scam['type']}"
            }
        
        # Word overlap matching (fuzzy)
        common_words = scam_words.intersection(input_words)
        # Ignore common words
        common_words -= {"loan", "bank", "india", "finance", "money", "cash"}
        
        if len(common_words) >= 2 or (len(common_words) == 1 and len(scam_words) <= 2):
            return {
                "match_found": True,
                "entity_type": scam["type"],
                "entity_name": scam["name"],
                "risk_score": scam["risk"],
                "is_scam": True,
                "message": f"⚠️ POSSIBLE MATCH: {scam['name']} - {scam['type']}"
            }
    
    # Check real banks
    for bank in SCAM_DATABASE["real_banks"]:
        bank_name_lower = bank["name"].lower()
        
        if bank_name_lower in name_lower or name_lower in bank_name_lower:
            return {
                "match_found": True,
                "entity_type": bank["type"],
                "entity_name": bank["name"],
                "risk_score": bank["risk"],
                "is_scam": False,
                "message": f"✅ VERIFIED: {bank['name']} - Legitimate {bank['type']}"
            }
        
        # Check abbreviations (SBI, HDFC, ICICI, etc.)
        abbreviations = {
            "state bank of india": ["sbi"],
            "hdfc bank": ["hdfc"],
            "icici bank": ["icici"],
            "axis bank": ["axis"],
            "punjab national bank": ["pnb"]
        }
        
        if bank_name_lower in abbreviations:
            for abbr in abbreviations[bank_name_lower]:
                if abbr in name_lower.split():
                    return {
                        "match_found": True,
                        "entity_type": bank["type"],
                        "entity_name": bank["name"],
                        "risk_score": bank["risk"],
                        "is_scam": False,
                        "message": f"✅ VERIFIED: {bank['name']} - Legitimate {bank['type']}"
                    }
    
    # No match found
    return {
        "match_found": False,
        "entity_type": "Unknown",
        "entity_name": name,
        "risk_score": 50,
        "is_scam": None,
        "message": "⚠️ NOT IN DATABASE - Proceed with caution"
    }


def check_blacklist(text: str) -> tuple[bool, str]:
    """
    Check if the text contains any blacklisted keywords.
    
    Returns:
        (is_blacklisted, matched_keyword)
    """
    text_lower = text.lower()
    for keyword in BLACKLISTED_KEYWORDS:
        if keyword in text_lower:
            return True, keyword
    return False, ""


def search_internet_for_scam(query: str, max_results: int = 3) -> list:
    """
    Search the internet for scam reports using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of search results with title, link, and snippet
    """
    try:
        ddgs = DDGS()
        results = []
        
        # Search with timeout
        search_results = ddgs.text(query, max_results=max_results, region='in-en', safesearch='off')
        
        for r in search_results:
            results.append({
                "title": r.get("title", ""),
                "link": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        
        return results
    except Exception as e:
        return []


def build_search_queries(initial_analysis: dict) -> list:
    """
    Build search queries based on initial AI analysis.
    
    Args:
        initial_analysis: Dict containing extracted entities and scam type
    
    Returns:
        List of search query strings
    """
    queries = []
    entities = initial_analysis.get("extracted_entities", {})
    scam_type = initial_analysis.get("scam_type", "")
    
    # Query 1: Company name + scam
    company = entities.get("company_name")
    if company and company.lower() not in ["null", "none", ""]:
        queries.append(f"{company} scam india fraud complaint")
    
    # Query 2: Phone number + scam
    phone = entities.get("phone_number")
    if phone and phone.lower() not in ["null", "none", ""]:
        queries.append(f"{phone} scam fraud india reports")
    
    # Query 3: Scam type specific
    if scam_type and scam_type.lower() not in ["null", "none", "n/a", "unknown", ""]:
        queries.append(f"{scam_type} india cybercrime alert")
    
    # Query 4: URL domain + phishing
    url = entities.get("url")
    if url and url.lower() not in ["null", "none", ""]:
        # Extract domain from URL
        domain = re.search(r'https?://([^/]+)', url)
        if domain:
            queries.append(f"{domain.group(1)} phishing scam india")
    
    # Fallback: Generic search if no entities
    if not queries:
        queries.append("online scam india cybercrime report 2025")
    
    return queries[:2]  # Return top 2 queries


def analyze_with_internet_search(image: Image.Image, api_key: str = None, language: str = "Hinglish") -> dict:
    """
    Enhanced analysis with internet search verification AND live database check.
    
    Args:
        image: PIL Image object of the screenshot
        api_key: Google Gemini API key (optional)
        language: Language for response
    
    Returns:
        dict with verdict, risk_score, search_results, live_db_results, and all analysis data
    """
    # Step 1: Initial AI analysis
    initial_result = analyze_screenshot(image, api_key, language)
    
    # If API error, return immediately
    if initial_result.get("verdict") == "ERROR":
        return initial_result
    
    # Step 2: Check against LIVE DATABASE first (fastest check)
    entities = initial_result.get("extracted_entities", {})
    phone_number = entities.get("phone_number")
    upi_id = entities.get("upi_id")
    
    live_db_hits = []
    live_db_boost = 0
    
    # Check phone number in live database
    if phone_number and phone_number.lower() not in ["null", "none", ""]:
        phone_check = check_phone(phone_number)
        if phone_check.get('found'):
            live_db_hits.append({
                'type': 'phone',
                'value': phone_number,
                'reports': phone_check['reports'],
                'last_seen': phone_check['last_seen'],
                'scam_types': phone_check['scam_types']
            })
            live_db_boost += 40  # Major boost for known scammer
            initial_result["red_flags"].append(f"🚨 LIVE ALERT: Number reported {phone_check['reports']} times!")
    
    # Check UPI ID in live database
    if upi_id and upi_id.lower() not in ["null", "none", ""]:
        upi_check = check_upi(upi_id)
        if upi_check.get('found'):
            live_db_hits.append({
                'type': 'upi',
                'value': upi_id,
                'reports': upi_check['reports'],
                'scam_types': upi_check['scam_types']
            })
            live_db_boost += 35
            initial_result["red_flags"].append(f"⚠️ UPI ID in scam database ({upi_check['reports']} reports)")
    
    # Apply live database boost
    if live_db_boost > 0:
        original_score = initial_result.get("risk_score", 50)
        new_score = min(100, original_score + live_db_boost)
        initial_result["risk_score"] = new_score
        initial_result["live_db_match"] = True
        
        # Force upgrade verdict for live database hits
        if len(live_db_hits) > 0:
            initial_result["verdict"] = "SCAM"
    else:
        initial_result["live_db_match"] = False
    
    initial_result["live_database"] = {
        "checked": True,
        "hits": live_db_hits,
        "total_hits": len(live_db_hits)
    }
    
    # Step 3: Build search queries from extracted data
    search_queries = build_search_queries(initial_result)
    
    # Step 4: Search internet for reports
    all_search_results = []
    search_start_time = time.time()
    
    for query in search_queries:
        try:
            results = search_internet_for_scam(query, max_results=3)
            if results:
                all_search_results.extend(results)
        except Exception as e:
            continue
    
    search_latency_ms = round((time.time() - search_start_time) * 1000, 2)
    
    # Step 5: Enhance verdict with search context
    if all_search_results:
        # Add search results to the response
        initial_result["internet_search"] = {
            "queries": search_queries,
            "results": all_search_results[:5],  # Top 5 results
            "sources_found": len(all_search_results),
            "search_latency_ms": search_latency_ms
        }
        
        # Analyze search results for scam indicators
        scam_keywords = ["scam", "fraud", "fake", "cheat", "beware", "警告", "सावधान"]
        scam_mentions = 0
        
        for result in all_search_results:
            text = (result.get("title", "") + " " + result.get("snippet", "")).lower()
            if any(keyword in text for keyword in scam_keywords):
                scam_mentions += 1
        
        # If search results confirm scam, increase risk score (but less than live DB)
        if scam_mentions >= 2:
            original_score = initial_result.get("risk_score", 50)
            new_score = min(100, original_score + 15)
            initial_result["risk_score"] = new_score
            initial_result["internet_verified"] = True
            initial_result["red_flags"].append(f"Internet reports confirm scam ({scam_mentions} sources)")
            
            # Upgrade verdict if needed (but not if already upgraded by live DB)
            if not initial_result.get("live_db_match"):
                if initial_result.get("verdict") == "SAFE" and new_score >= 60:
                    initial_result["verdict"] = "SUSPICIOUS"
                elif initial_result.get("verdict") == "SUSPICIOUS" and new_score >= 85:
                    initial_result["verdict"] = "SCAM"
        else:
            initial_result["internet_verified"] = False
    else:
        initial_result["internet_search"] = {
            "queries": search_queries,
            "results": [],
            "sources_found": 0,
            "search_latency_ms": search_latency_ms
        }
        initial_result["internet_verified"] = False
    
    return initial_result


def generate_cyber_complaint(scam_details: dict) -> bytes:
    """
    Generate a formal cyber complaint PDF for reporting scams.
    
    Args:
        scam_details: Dictionary containing:
            - scam_type: Type of scam detected
            - phone_number: Scammer's phone number (if extracted)
            - company_name: Fake company name (if any)
            - amount: Amount mentioned (if any)
            - extracted_text: OCR text from screenshot
            - risk_score: AI-assigned risk score
            - red_flags: List of detected red flags
            - reasoning: AI's reasoning
            - user_profile: Dictionary with name, contact, email, address, city, state
    
    Returns:
        PDF as bytes for download
    """
    from fpdf import FPDF
    from datetime import datetime
    import io
    
    # Extract details with fallbacks
    scam_type = scam_details.get("scam_type", "[Unknown Scam Type]")
    phone_number = scam_details.get("phone_number") or "[Unknown Number]"
    company_name = scam_details.get("company_name") or "[Unknown Entity]"
    amount = scam_details.get("amount") or "[Amount Not Specified]"
    extracted_text = scam_details.get("extracted_text") or "[Screenshot text not available]"
    risk_score = scam_details.get("risk_score", 0)
    red_flags = scam_details.get("red_flags", [])
    reasoning = scam_details.get("reasoning") or "[AI analysis not available]"
    
    # Extract user profile (with fallbacks for backward compatibility)
    user_profile = scam_details.get("user_profile", {})
    user_name = user_profile.get("name", "[Your Name]")
    user_contact = user_profile.get("contact", "[Your Contact Number]")
    user_email = user_profile.get("email", "[Your Email Address]")
    user_address = user_profile.get("address", "[Your Address]")
    user_city = user_profile.get("city", "[City Name]")
    user_state = user_profile.get("state", "[State]")
    
    current_date = datetime.now().strftime("%d %B %Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "OFFICIAL COMPLAINT - CYBER CRIME REPORT", ln=True, align="C")
    pdf.ln(5)
    
    # Reference Number
    pdf.set_font("Helvetica", "", 10)
    ref_no = f"SATARK/{datetime.now().strftime('%Y%m%d%H%M%S')}"
    pdf.cell(0, 5, f"Reference No: {ref_no}", ln=True, align="R")
    pdf.cell(0, 5, f"Date: {current_date}", ln=True, align="R")
    pdf.ln(10)
    
    # To Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "To:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, f"The Nodal Officer,\nCyber Crime Cell,\n{user_city}, {user_state}\nNational Cyber Crime Reporting Portal")
    pdf.ln(5)
    
    # Subject
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Subject: Reporting Financial Fraud Attempt via WhatsApp/SMS", ln=True)
    pdf.ln(5)
    
    # Salutation
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Respected Sir/Madam,", ln=True)
    pdf.ln(3)
    
    # Body Paragraph 1
    body_para1 = f"I am writing to formally report a suspected financial fraud attempt that I received on {current_date} at approximately {current_time}. The sender, identified as {phone_number}, attempted to defraud me using the pretext of \"{scam_type}\"."
    pdf.multi_cell(0, 6, body_para1)
    pdf.ln(3)
    
    # Body Paragraph 2
    if company_name != "[Unknown Entity]":
        body_para2 = f"The fraudulent message impersonated \"{company_name}\" and mentioned an amount of {amount}. This is a clear attempt to deceive unsuspecting citizens."
    else:
        body_para2 = f"The message contained suspicious content mentioning {amount}. This is a clear attempt to deceive unsuspecting citizens."
    pdf.multi_cell(0, 6, body_para2)
    pdf.ln(5)
    
    # AI Analysis Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "AI ANALYSIS REPORT (Satark.ai):", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, f"- Risk Score: {risk_score}/100 (HIGH RISK)", ln=True)
    pdf.cell(0, 5, f"- Scam Type: {scam_type}", ln=True)
    
    if red_flags:
        pdf.cell(0, 5, "- Red Flags Detected:", ln=True)
        for flag in red_flags[:5]:  # Limit to 5 flags
            # Sanitize text for PDF
            safe_flag = flag.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 5, f"    * {safe_flag}", ln=True)
    pdf.ln(3)
    
    # Reasoning
    pdf.set_font("Helvetica", "I", 10)
    safe_reasoning = reasoning.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 5, f"AI Reasoning: {safe_reasoning}")
    pdf.ln(5)
    
    # Evidence Section
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "EXHIBIT A - EXTRACTED MESSAGE CONTENT:", ln=True)
    pdf.set_font("Courier", "", 9)
    
    # Sanitize and truncate extracted text
    safe_text = extracted_text.encode('latin-1', 'replace').decode('latin-1')
    if len(safe_text) > 800:
        safe_text = safe_text[:800] + "... [truncated]"
    
    # Draw bordered box for evidence
    pdf.set_draw_color(100, 100, 100)
    pdf.set_fill_color(245, 245, 245)
    x = pdf.get_x()
    y = pdf.get_y()
    pdf.multi_cell(0, 4, safe_text, border=1, fill=True)
    pdf.ln(5)
    
    # Request Section
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, "I kindly request you to:\n1. Register an FIR against the perpetrator(s)\n2. Investigate and trace the fraudulent sender\n3. Take necessary action to prevent others from being victimized\n4. Block the reported phone number/UPI ID if applicable")
    pdf.ln(5)
    
    # Declaration
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(0, 5, "I hereby declare that the information provided above is true to the best of my knowledge. I am willing to cooperate with the investigation as required.")
    pdf.ln(10)
    
    # Signature Section
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Yours faithfully,", ln=True)
    pdf.ln(8)
    pdf.cell(0, 6, user_name, ln=True)
    pdf.cell(0, 6, user_contact, ln=True)
    pdf.cell(0, 6, user_email, ln=True)
    pdf.cell(0, 6, user_address, ln=True)
    pdf.ln(10)
    
    # Footer
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 4, "This complaint was generated using Satark.ai - AI-Powered Scam Detection", ln=True, align="C")
    pdf.cell(0, 4, "National Cyber Crime Helpline: 1930 | cybercrime.gov.in", ln=True, align="C")
    
    # Output to bytes
    return bytes(pdf.output())
