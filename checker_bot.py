import os
import time
import random
from dotenv import load_dotenv
from datetime import datetime
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

def sendEmail(mail_content, sender_address, sender_pass, receiver_address):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'ICBC Bot Notification'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return 'Mail Sent\n' + mail_content

def load_appointments(file_path):
    appointments = {}
    if not os.path.exists(file_path):
        return appointments

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            location = row["Location"]
            date_time = f"{row['Date']} {row['Time']}"
            if location not in appointments:
                appointments[location] = []
            appointments[location].append(date_time)
    return appointments

def check_for_earlier_slots(old_appointments, new_appointments):
    earlier_slots = {}
    for location, new_slots in new_appointments.items():
        old_slots = old_appointments.get(location, [])
        old_earliest = min(old_slots, default=None)
        for new_date_time in new_slots:
            if old_earliest is None or new_date_time < old_earliest:
                if location not in earlier_slots:
                    earlier_slots[location] = []
                earlier_slots[location].append(new_date_time)
    return earlier_slots

def get_day_of_week(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A")

def format_mail_content(earlier_slots):
    mail_content = "Earlier time slots found:\n\n"
    for location, slots in earlier_slots.items():
        mail_content += f"Location: {location}\n"
        for slot in slots:
            date_str, time_str = slot.split()
            day_of_week = get_day_of_week(date_str)
            mail_content += f" - {date_str} ({day_of_week}) {time_str}\n"
        mail_content += "\n"
    return mail_content

def main():
    # Fetch configuration from environment variables
    sender_address = os.getenv('GMAIL_SENDER_ADDRESS')
    sender_pass = os.getenv('GMAIL_SENDER_PASS')
    receiver_address = os.getenv('GMAIL_RECEIVER_ADDRESS')

    old_appointments = load_appointments('appointments.csv')

    os.system('python icbc-appointment.py')

    new_appointments = load_appointments('appointments.csv')

    earlier_slots = check_for_earlier_slots(old_appointments, new_appointments)

    if earlier_slots:
        mail_content = format_mail_content(earlier_slots)
        print(sendEmail(mail_content, sender_address, sender_pass, receiver_address))
    else:
        print("No earlier time slots found.")

if __name__ == "__main__":
    while True:
        main()
        wait_time = random.uniform(180, 300)  # Vary the frequency of running the appointment code
        print(f"Waiting for {wait_time:.2f} seconds before running the next check...")  # Debugging message
        time.sleep(wait_time)