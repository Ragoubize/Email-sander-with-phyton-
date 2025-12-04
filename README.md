# 📧 Python Bulk HTML Email Sender

A lightweight, secure, and customizable Python script designed to send HTML-formatted emails to a list of recipients using the SMTP protocol. This tool separates configuration, content, and logic, making it easy to manage and deploy.

## 🚀 Features

-   **HTML Support:** Sends rich text emails using an HTML template.
-   **Secure Connection:** Uses `ssl` and `starttls` to encrypt the SMTP connection.
-   **Configurable:** Keeps sensitive credentials (passwords, server details) separate from the code.
-   **Personalized Sending:** Iterates through the recipient list, sending individual emails to ensure privacy (recipients cannot see each other).
-   **Rate Limiting:** Includes a delay mechanism to prevent being flagged as spam by email servers.
-   **No External Dependencies:** Uses only Python's standard libraries.

## 📂 Project Structure

Here is an explanation of the files included in this project:

### 1. `send_emails.py` (The Main Script)
This is the core logic of the application.
-   **Function:** It orchestrates the entire process.
-   **How it works:**
    1.  Loads settings from `config.ini`.
    2.  Reads email addresses from `recipients.txt`.
    3.  Reads the HTML content from `message.html`.
    4.  Connects to the SMTP server defined in the config.
    5.  Loops through the recipients and sends the email individually.

### 2. `config.ini` (Configuration)
Contains the sensitive settings for the SMTP server.
-   **Role:** Separation of concerns. You don't hardcode passwords in the Python script.
-   **Content:** Server address (e.g., `smtp.gmail.com`), port, username, password, and sender email.

### 3. `recipients.txt` (Contact List)
A simple text file containing the target email addresses.
-   **Format:** One email address per line.
-   **Logic:** The script automatically strips empty lines and whitespace.

### 4. `message.html` (Email Body)
The template for the email content.
-   **Role:** Allows you to design the email using HTML/CSS.
-   **Feature:** Supports UTF-8 encoding (works with Arabic, English, emojis, etc.).

---

## ⚙️ Setup & Configuration

### 1. Clone the Repository
```bash
git clone https://github.com/Ragoubize/Email-sander-with-phyton-.git
