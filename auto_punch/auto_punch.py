"""Automatically check in."""
import json
import logging
import secrets
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pendulum

# Load required files
with (Path(__file__).parent / "working_day_2024.json").open("r") as f:
    calendar_list = json.load(f)
with (Path(__file__).parent / "secret.json").open("r") as f:
    smtp_secret = json.load(f)

# SMTP server information
MAIL_SERVER = smtp_secret.get("MAIL_SERVER")
SMTP_PORT = int(smtp_secret.get("SMTP_PORT"))
EMAIL_USERNAME = smtp_secret.get("EMAIL_USERNAME")
EMIAL_PASSWORD = smtp_secret.get("EMIAL_PASSWORD")

# Email details
PUNCH_EMAIL = smtp_secret.get("PUNCH_EMAIL")
SENDER_EMAIL = EMAIL_USERNAME

# Punch in/out waiting time
THIRTY_MIN_SEC = 1700


def send_empty_email(receiver_email: str) -> bool:
    """send_email."""
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = ""

    # Add body to email
    message.attach(MIMEText("", "plain"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(MAIL_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection with TLS
            server.login(EMAIL_USERNAME, EMIAL_PASSWORD)
            text = message.as_string()
            server.sendmail(SENDER_EMAIL, receiver_email, text)

            logging.info("Email sent!")

            return True
    except smtplib.SMTPResponseException:
        logging.exception("Failed to send email!")
        return False


def is_working_day() -> bool:
    """is_working_day."""
    today_yyyymmdd = pendulum.now(tz="Asia/Taipei").strftime("%Y%m%d")
    for day_info_dict in calendar_list:
        if day_info_dict.get("西元日期", "") == today_yyyymmdd:
            if day_info_dict.get("是否放假") == "0": # "0" -> True, "2" -> False
                return True
            break
    return False

def wait_for_punch() -> None:
    """wait_for_punch."""
    waiting_time = secrets.randbelow(THIRTY_MIN_SEC) + 1
    logging.info("Wait for %s seconds.", waiting_time)
    time.sleep(waiting_time)


def punch() -> bool:
    """punch."""
    return send_empty_email(PUNCH_EMAIL)


def backup() -> bool:
    """backup."""
    return send_empty_email(EMAIL_USERNAME)


if __name__ == "__main__":
    if is_working_day():
        wait_for_punch()
        punch()
        backup()
