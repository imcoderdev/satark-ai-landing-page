# 📧 Email Alert Setup Guide

## Automatic Email Alerts for Scam Detection

Your Satark.ai app now automatically sends email alerts to **mistyraju0@gmail.com** when a scam is detected!

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Enable Gmail App Passwords

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** in the left sidebar
3. Enable **2-Step Verification** (if not already enabled)
4. Scroll down and click **App passwords**
5. Select app: **Mail**
6. Select device: **Other (Custom name)** → type "Satark.ai"
7. Click **Generate**
8. Copy the 16-character app password (e.g., `abcd efgh ijkl mnop`)

### Step 2: Update .env File

Edit the `.env` file and add your credentials:

```env
GMAIL_SENDER=your-email@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
```

**Important:** 
- Remove spaces from the app password
- Use your actual Gmail address
- Keep this file private (it's in .gitignore)

### Step 3: Test the Email System

Run this command to test if emails are working:

```python
python -c "from email_alerts import send_test_email; send_test_email('mistyraju0@gmail.com')"
```

You should receive a test email at mistyraju0@gmail.com!

---

## 🎯 How It Works

1. **User uploads screenshot** → Satark.ai analyzes it
2. **If SCAM detected** → Automatic email sent to mistyraju0@gmail.com
3. **Email contains:**
   - Risk score & verdict
   - Scam type (Lottery, Phishing, Loan Fraud, etc.)
   - Red flags detected
   - Extracted phone numbers, UPI IDs, amounts
   - Recommended actions

---

## 📨 Email Features

✅ **Professional HTML email** with color-coded alerts  
✅ **Risk score visualization** (0-100%)  
✅ **Detailed red flags** and analysis  
✅ **Extracted scammer information** (phone, UPI, URLs)  
✅ **Action recommendations** (block, report, delete)  
✅ **Timestamp** of detection  

---

## 🛠️ Troubleshooting

### Email not sending?

**Check 1: Credentials in .env**
```bash
# Verify your .env file has:
GMAIL_SENDER=youremail@gmail.com
GMAIL_APP_PASSWORD=yourapppassword
```

**Check 2: App Password is correct**
- Must be 16 characters (no spaces)
- Generated from Google Account > Security > App passwords
- Not your regular Gmail password

**Check 3: 2-Step Verification**
- Must be enabled on your Google Account
- Required to create app passwords

**Check 4: Test manually**
```python
from email_alerts import send_test_email
send_test_email('mistyraju0@gmail.com')
```

### Error: "Username and Password not accepted"
- You're using your regular password instead of App Password
- Generate a new App Password from Google Account settings

### Error: "SMTP Authentication Error"
- Check if 2-Step Verification is enabled
- Regenerate App Password
- Make sure no spaces in the password

---

## 🔒 Security Notes

1. **Never share your App Password** - it's like your email password
2. **Use environment variables** - keep `.env` file private
3. **App Passwords are safer** than using your main password
4. **Revoke if compromised** - You can revoke app passwords anytime

---

## 🌐 For Google Cloud Deployment

When deploying to Cloud Run, add environment variables:

```bash
gcloud run deploy satark-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY="your-api-key",GMAIL_SENDER="your-email@gmail.com",GMAIL_APP_PASSWORD="your-app-password"
```

Or use Secret Manager (more secure):
```bash
# Create secrets
echo -n "your-email@gmail.com" | gcloud secrets create gmail-sender --data-file=-
echo -n "your-app-password" | gcloud secrets create gmail-app-password --data-file=-

# Deploy with secrets
gcloud run deploy satark-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-secrets=GMAIL_SENDER=gmail-sender:latest,GMAIL_APP_PASSWORD=gmail-app-password:latest
```

---

## 📝 Customization

### Change recipient email

Edit `app.py` line where email is sent:
```python
email_sent = send_scam_alert_email(result, recipient_email="newemail@gmail.com")
```

### Send to multiple recipients

Edit `email_alerts.py` and modify the function:
```python
recipients = ["mistyraju0@gmail.com", "admin@company.com"]
for recipient in recipients:
    send_scam_alert_email(scam_details, recipient)
```

### Add SMS alerts

Integrate Twilio or other SMS services in `email_alerts.py`

---

## ✅ Testing Checklist

- [ ] 2-Step Verification enabled on Gmail
- [ ] App Password generated
- [ ] .env file updated with credentials
- [ ] Test email sent successfully
- [ ] Scam detection triggers email
- [ ] Email received at mistyraju0@gmail.com
- [ ] Email has proper formatting

---

## 📧 Sample Email Preview

```
Subject: 🚨 SCAM ALERT: Lottery Scam Detected - Risk Score: 95

[Header with gradient background]
🛡️ Satark.ai Scam Alert
A potential scam has been detected and analyzed

🚨 Verdict: SCAM
95% Risk

📋 Scam Type: Lottery Scam

🧠 Analysis:
This message shows classic lottery scam patterns...

🚩 Red Flags Detected:
• Urgent threatening language detected
• Requests upfront fees before payout
• Grammar mistakes and typos

📊 Extracted Information:
• Company Name: Lucky Winners Ltd
• Phone Number: +91 98765 43210
• Amount: ₹50,00,000
• UPI ID: scammer@paytm

💡 Recommended Actions:
✅ Block the sender immediately
✅ Do not respond or share any personal information
✅ Report to Cyber Crime Portal
✅ Delete the message/app
```

---

Need help? Check the console output for detailed error messages!
