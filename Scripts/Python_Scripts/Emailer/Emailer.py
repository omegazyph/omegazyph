import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

def send_email():
    # Get email credentials
    sender_email = input("Enter your email address: ")
    password = getpass("Enter your email password: ")
    recipient_email = input("Enter recipient email address: ")

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = input("Enter email subject: ")

    # Add message body
    message_body = input("Enter email message: ")
    message.attach(MIMEText(message_body, "plain"))

    try:
        # Connect to SMTP server
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        
        # Login to email account
        smtp_server.login(sender_email, password)
        
        # Send email
        smtp_server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
        
        # Close connection
        smtp_server.quit()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    send_email()
