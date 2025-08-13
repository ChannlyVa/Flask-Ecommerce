import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
from tabulate import tabulate

mail = Mail()

def init_mail(app):
    # Explicitly load .env from this file's directory
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(dotenv_path=env_path)

    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")

    print("MAIL_USERNAME from env:", mail_username)   # Debug print
    print("MAIL_PASSWORD from env:", mail_password is not None)  # Debug print

    if not mail_username or not mail_password:
        raise RuntimeError("MAIL_USERNAME or MAIL_PASSWORD not set in environment variables.")

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = mail_username
    app.config['MAIL_PASSWORD'] = mail_password
    app.config['MAIL_DEFAULT_SENDER'] = mail_username

    mail.init_app(app)

def send_order_email(to_email, fullName, phone, address, item_list, total):
    sender_email = os.getenv("MAIL_USERNAME")

    html_content = (
        f"<strong>Confirm Your Order</strong><br>"
        f"<strong>---------------------------------------------------------------------</strong><br>"
        f"<strong>Name: {fullName}</strong><br>"
        f"<strong>Phone: {phone}</strong><br>"
        f"<strong>Email: {to_email}</strong><br>"
        f"<strong>Address: {address}</strong><br>"
        f"<strong>---------------------------------------------------------------------</strong><br>"
        f"<pre>{tabulate(item_list, headers=['No', 'Title', 'Price', 'QTY'], numalign='left', stralign='left', floatfmt='.2f')}</pre><br>"
        f"<strong>---------------------------------------------------------------------</strong><br>"
        f"<strong>Total : ${total:.2f}</strong><br>"
    )

    msg = Message(
        subject="Your Order Confirmation",
        recipients=[to_email],
        sender=sender_email
    )
    msg.html = html_content
    mail.send(msg)
