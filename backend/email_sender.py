# email_sender.py - Send PDF report via email

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(to_email: str, pdf_bytes: bytes, query: str) -> str:
    """
    Send the PDF report via email.
    Requires environment variables: EMAIL_USER and EMAIL_PASS
    """
    try:
        # Email credentials (set in environment variables for security)
        sender_email = os.getenv("EMAIL_USER", "your_email@gmail.com")
        sender_password = os.getenv("EMAIL_PASS", "your_app_password")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"InsightLoop.AI Report: {query[:50]}..."

        # Body
        body = f"""
Dear User,

Attached is your InsightLoop.AI research report for the query: "{query}"

This report was generated autonomously using web crawling and AI summarization.

Best regards,
InsightLoop.AI Team
"""
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(pdf_bytes)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename='insightloop_report.pdf')
        msg.attach(attachment)

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()

        return f"Report sent successfully to {to_email}!"

    except Exception as e:
        return f"Failed to send email: {str(e)}"
