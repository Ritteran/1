"""
Email Sender Module for NSE/BSE Scraper Newsletter
Sends daily summaries via Gmail SMTP
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSender:
    """Handles email sending via Gmail SMTP"""

    def __init__(self):
        """Initialize email configuration from environment variables"""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_ADDRESS")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")

        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)

        # Validate configuration
        self._validate_config()

    def _validate_config(self):
        """Validate that all required email configuration is present"""
        if not self.sender_email:
            raise ValueError("GMAIL_ADDRESS not set in environment variables")
        if not self.sender_password:
            raise ValueError("GMAIL_APP_PASSWORD not set in environment variables")
        if not self.recipient_email:
            raise ValueError("RECIPIENT_EMAIL not set in environment variables")

    def send_newsletter(self, subject, body):
        """
        Send plain text newsletter email

        Args:
            subject (str): Email subject line
            body (str): Plain text email body

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = subject

            # Add body
            message.attach(MIMEText(body, "plain"))

            # Connect to Gmail SMTP server
            self.logger.info(f"Connecting to {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.sender_password)

                # Send email
                server.send_message(message)

            self.logger.info(f"Newsletter sent successfully to {self.recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            self.logger.error("Gmail authentication failed. Check your app password.")
            return False
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error occurred: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    def send_error_notification(self, error_message):
        """
        Send error notification email

        Args:
            error_message (str): Error details to send

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        subject = f"NSE/BSE Scraper Error - {datetime.now().strftime('%Y-%m-%d')}"
        body = f"""
NSE/BSE Daily Scraper Error Report
{'=' * 50}

An error occurred during the scheduled scraping run:

{error_message}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check the logs for more details.
"""
        return self.send_newsletter(subject, body)


if __name__ == "__main__":
    # Test the email sender
    logging.basicConfig(level=logging.INFO)

    sender = EmailSender()
    test_subject = "Test Email - NSE/BSE Scraper"
    test_body = "This is a test email from the NSE/BSE scraper system."

    if sender.send_newsletter(test_subject, test_body):
        print("Test email sent successfully!")
    else:
        print("Failed to send test email. Check logs.")
