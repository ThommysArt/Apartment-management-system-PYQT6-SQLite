import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    try:
        context = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        context.login(sender_email, sender_password)
        context.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

    finally:
        context.quit()


'''
sender_email = "your_email@gmail.com"
sender_password = "your_password"
recipient_email = "recipient_email@example.com"
subject = "Hello from Python!"
message = "This is a test email sent from Python."
'''


def send_reminder_email(recipient_email, subject, message):
    with open('account.txt', 'r') as f:
        sender_email = f.readline(0)
        sender_password = f.readline(1)

    send_email(sender_email=sender_email, sender_password=sender_password, subject=subject, recipient_email=recipient_email, message=message)

