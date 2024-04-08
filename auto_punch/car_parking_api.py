#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging, ngrok
import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pendulum


# Load required files
with (Path(__file__).parent / "secret.json").open("r") as f:
    user_secret = json.load(f)
with (Path(__file__).parent / "car_parking_table_html_tamplate.html").open("r") as f:
    car_parking_table_html_tamplate = f.read()

# SMTP server information
MAIL_SERVER = user_secret.get("MAIL_SERVER")
SMTP_PORT = int(user_secret.get("SMTP_PORT"))
EMAIL_USERNAME = user_secret.get("EMAIL_USERNAME")
EMIAL_PASSWORD = user_secret.get("EMIAL_PASSWORD")

# Email details
CAR_PARKING_EMAIL = user_secret.get("CAR_PARKING_EMAIL")
SENDER_EMAIL = EMAIL_USERNAME

# Car parking information
WEEKDAY_MAP = {
    "1": "星期一",
    "2": "星期二",
    "3": "星期三",
    "4": "星期四",
    "5": "星期五",
}
TODAY_DATETIME = pendulum.now(tz="Asia/Taipei")
TOMORROW_DATETIME = TODAY_DATETIME.add(days=1)
TODAY_DATE_STR = TODAY_DATETIME.strftime("%Y/%m/%d")
TOMORROW_DATE_STR = TOMORROW_DATETIME.strftime("%Y/%m/%d")
TOMORROW_WEEKDAY_STR = WEEKDAY_MAP.get(TOMORROW_DATETIME.strftime("%w"))
CAR_PARKING_VISITOR = user_secret.get("CAR_PARKING_VISITOR")
CAR_NUMBER = user_secret.get("CAR_NUMBER")
CAR_PARKING_EMAIL = user_secret.get("CAR_PARKING_EMAIL")

# Car parking form HTML
car_parking_table_html = car_parking_table_html_tamplate.format(
    TODAY_DATE_STR=TODAY_DATE_STR,
    CAR_PARKING_VISITOR=CAR_PARKING_VISITOR,
    TOMORROW_DATE_STR=TOMORROW_DATE_STR,
    TOMORROW_WEEKDAY_STR=TOMORROW_WEEKDAY_STR,
    CAR_NUMBER=CAR_NUMBER,
)


def send_empty_email(receiver_email: str) -> bool:
    """send_email."""
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = "臨時停車預約"

    # Add body to email
    message.attach(MIMEText(car_parking_table_html, "html"))

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


def reserve_car_parking() -> bool:
    """reserve_car_parking."""
    return send_empty_email(CAR_PARKING_EMAIL)


def backup() -> bool:
    """backup."""
    # return send_empty_email(EMAIL_USERNAME)
    return send_empty_email("allenshi@hlh.com.tw,aegis12321@gmail.com")


def car_parking_reservation_main() -> None:
    """car_parking_reservation_main."""
    reserve_car_parking()
    backup()

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = bytes("Hello", "utf-8")
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        car_parking_reservation_main()
        self.wfile.write(body)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = HTTPServer(("localhost", 0), HelloHandler)
    ngrok.listen(server)
    server.serve_forever()

    car_parking_reservation_main()
