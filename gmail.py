import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml

def sendEmail(mail_content, sender_address, sender_pass, receiver_address):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'ICBC New Available Test Notification'
    message.attach(MIMEText(mail_content, 'plain'))
    
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail with port
    session.starttls()  # Enable security
    session.login(sender_address, sender_pass)  # Login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return 'Mail Sent\n' + mail_content