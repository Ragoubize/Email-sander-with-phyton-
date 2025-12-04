import smtplib
import ssl
import time
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Configuration files ---
CONFIG_FILE = 'config.ini'
RECIPIENTS_FILE = 'recipients.txt'
MESSAGE_FILE = 'message.html'

def load_config():
    """Load SMTP settings from config.ini"""
    config = configparser.ConfigParser()
    if not config.read(CONFIG_FILE):
        print(f"Error: Settings file '{CONFIG_FILE}' not found. Make sure it exists in the same folder.")
        exit()
    try:
        return config['smtp']
    except KeyError:
        print(f"Error: The file '{CONFIG_FILE}' must contain a [smtp] section.")
        exit()

def load_recipients():
    """Load list of email recipients from a text file"""
    try:
        with open(RECIPIENTS_FILE, 'r') as f:
            # Clean list from empty lines and extra spaces
            recipients = [line.strip() for line in f if line.strip()]
        if not recipients:
            print(f"Error: Recipient file '{RECIPIENTS_FILE}' is empty.")
            exit()
        return recipients
    except FileNotFoundError:
        print(f"Error: Recipient file '{RECIPIENTS_FILE}' not found.")
        exit()

def load_message_template():
    """Load HTML message template"""
    try:
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Message file '{MESSAGE_FILE}' not found.")
        exit()

def main():
    # Load settings and recipient list
    smtp_config = load_config()
    recipients = load_recipients()
    html_template = load_message_template()

    # Extract SMTP information
    server_host = smtp_config.get('server')
    server_port = smtp_config.getint('port')
    username = smtp_config.get('username')
    password = smtp_config.get('password')
    sender_email = smtp_config.get('sender_email')
    
    # Ask user to input the email subject
    subject = input("Please enter the email subject: ")
    
    # Set fallback plain text message
    plain_text_fallback = "This message requires an HTML-compatible email client."

    print(f"\nFound {len(recipients)} email(s). Starting the sending process...")
    
    # Create secure SSL context
    context = ssl.create_default_context()
    
    try:
        # 'with' ensures the connection is closed automatically
        with smtplib.SMTP(server_host, server_port) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(username, password)  # Login
            
            # Loop to send the email to each recipient
            for i, recipient_email in enumerate(recipients):
                # Create a separate message object for each recipient
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = recipient_email  # Important: ensures each recipient sees only their email

                # Attach the plain text first, then the HTML
                message.attach(MIMEText(plain_text_fallback, "plain"))
                message.attach(MIMEText(html_template, "html"))

                try:
                    server.sendmail(
                        sender_email, recipient_email, message.as_string()
                    )
                    print(f"({i+1}/{len(recipients)}) Successfully sent to: {recipient_email}")
                except Exception as e:
                    print(f"({i+1}/{len(recipients)}) Failed to send to: {recipient_email}. Error: {e}")
                
                # Small delay to avoid IP bans
                time.sleep(1)  # Wait 1 second between each send

    except smtplib.SMTPAuthenticationError:
        print("\nAuthentication error: Check the username and password in config.ini.")
    except Exception as e:
        print(f"\nA general error occurred while connecting to the server: {e}")

    print("\n--- Sending process completed ---")

if __name__ == "__main__":
    main()
