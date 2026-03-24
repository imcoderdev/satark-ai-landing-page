"""
Email notification utility for Satark.ai
Sends alerts when scams are detected
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


def send_scam_alert_email(scam_details: dict, recipient_email: str = "mistyraju0@gmail.com"):
    """
    Send email alert when scam is detected
    
    Args:
        scam_details: Dictionary containing scam analysis results
        recipient_email: Email address to send alert to
    """
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Use configured credentials
        sender_email = "kalen5471@gmail.com"
        sender_password = "qbodchmvakgmvueh"
        
        # Extract scam details
        verdict = scam_details.get("verdict", "UNKNOWN")
        risk_score = scam_details.get("risk_score", 0)
        scam_type = scam_details.get("scam_type", "Unknown")
        red_flags = scam_details.get("red_flags", [])
        reasoning = scam_details.get("reasoning", "No details available")
        entities = scam_details.get("extracted_entities", {})
        
        # Create email message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🚨 SCAM ALERT: {scam_type} Detected - Risk Score: {risk_score}"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Create HTML email body
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #d32f2f, #f44336); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; border-radius: 10px; margin-top: 20px; }}
                .risk-score {{ font-size: 48px; font-weight: bold; color: #d32f2f; text-align: center; margin: 20px 0; }}
                .red-flags {{ background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0; }}
                .entities {{ background: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 15px 0; }}
                .footer {{ text-align: center; color: #666; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
                ul {{ list-style-type: none; padding-left: 0; }}
                li {{ padding: 5px 0; }}
                .label {{ font-weight: bold; color: #555; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛡️ Satark.ai Scam Alert</h1>
                <p>A potential scam has been detected and analyzed</p>
            </div>
            
            <div class="content">
                <h2>🚨 Verdict: {verdict}</h2>
                <div class="risk-score">{risk_score}% Risk</div>
                
                <h3>📋 Scam Type:</h3>
                <p><strong>{scam_type}</strong></p>
                
                <h3>🧠 Analysis:</h3>
                <p>{reasoning}</p>
                
                <div class="red-flags">
                    <h3>🚩 Red Flags Detected:</h3>
                    <ul>
                        {''.join([f'<li>• {flag}</li>' for flag in red_flags])}
                    </ul>
                </div>
                
                <div class="entities">
                    <h3>📊 Extracted Information:</h3>
                    <ul>
                        <li><span class="label">Company Name:</span> {entities.get('company_name', 'Not found')}</li>
                        <li><span class="label">Phone Number:</span> {entities.get('phone_number', 'Not found')}</li>
                        <li><span class="label">Amount:</span> {entities.get('amount', 'Not found')}</li>
                        <li><span class="label">UPI ID:</span> {entities.get('upi_id', 'Not found')}</li>
                        <li><span class="label">URL:</span> {entities.get('url', 'Not found')}</li>
                    </ul>
                </div>
                
                <h3>💡 Recommended Actions:</h3>
                <ul>
                    <li>✅ Block the sender immediately</li>
                    <li>✅ Do not respond or share any personal information</li>
                    <li>✅ Report to Cyber Crime Portal: https://cybercrime.gov.in</li>
                    <li>✅ Delete the message/app</li>
                    <li>✅ Alert your contacts about this scam</li>
                </ul>
            </div>
            
            <div class="footer">
                <p><strong>Satark.ai - Your Financial Bodyguard 🛡️</strong></p>
                <p>Detected at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")}</p>
                <p><em>This is an automated alert from Satark.ai scam detection system</em></p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version (fallback)
        text_body = f"""
SATARK.AI SCAM ALERT
====================

VERDICT: {verdict}
RISK SCORE: {risk_score}%
SCAM TYPE: {scam_type}

ANALYSIS:
{reasoning}

RED FLAGS:
{chr(10).join([f'- {flag}' for flag in red_flags])}

EXTRACTED INFORMATION:
- Company Name: {entities.get('company_name', 'Not found')}
- Phone Number: {entities.get('phone_number', 'Not found')}
- Amount: {entities.get('amount', 'Not found')}
- UPI ID: {entities.get('upi_id', 'Not found')}
- URL: {entities.get('url', 'Not found')}

RECOMMENDED ACTIONS:
✅ Block the sender immediately
✅ Do not respond or share any personal information
✅ Report to Cyber Crime Portal: https://cybercrime.gov.in
✅ Delete the message/app
✅ Alert your contacts about this scam

---
Detected at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")}
Satark.ai - Your Financial Bodyguard 🛡️
        """
        
        # Attach both versions
        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print(f"✅ Scam alert email sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False


def send_test_email(recipient_email: str = "mistyraju0@gmail.com"):
    """Send a test email to verify configuration"""
    test_details = {
        "verdict": "SCAM",
        "risk_score": 95,
        "scam_type": "Test Alert - Lottery Scam",
        "reasoning": "This is a test email from Satark.ai to verify email configuration is working correctly.",
        "red_flags": [
            "Test flag 1: Urgent language detected",
            "Test flag 2: Requests for upfront fees",
            "Test flag 3: Fake lottery notification"
        ],
        "extracted_entities": {
            "company_name": "Test Lottery Corp",
            "phone_number": "+91 98765 43210",
            "amount": "₹50,00,000",
            "upi_id": "scammer@paytm",
            "url": "http://fake-lottery.com"
        }
    }
    
    return send_scam_alert_email(test_details, recipient_email)
