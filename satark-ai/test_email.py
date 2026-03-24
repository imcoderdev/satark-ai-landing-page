"""
Quick test script to verify email sending works
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_email():
    sender_email = "kalen5471@gmail.com"
    sender_password = "qbodchmvakgmvueh"
    target_email = "mistyraju0@gmail.com"
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = target_email
        msg['Subject'] = 'Test Email from Satark.ai'
        
        body = f"""
This is a test email sent at {datetime.now()}.

If you receive this, the email system is working correctly!

- Satark.ai Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        print("Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(sender_email, sender_password)
        
        print("Sending email...")
        server.send_message(msg)
        
        print("Closing connection...")
        server.quit()
        
        print(f"✅ Email sent successfully to {target_email}!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_email()
