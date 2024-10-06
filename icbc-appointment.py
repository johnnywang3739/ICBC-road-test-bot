import os
import requests
import json
from datetime import datetime
import csv
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from the environment variables
lastName = os.getenv('ICBC_LASTNAME')
licenceNumber = os.getenv('ICBC_LICENCENUMBER')
keyword = os.getenv('ICBC_KEYWORD')
expactAfterDate = os.getenv('ICBC_EXPECT_AFTERDATE')
expactBeforeDate = os.getenv('ICBC_EXPECT_BEFOREDATE')
expactAfterTime = os.getenv('ICBC_EXPECT_AFTERTIME')
expactBeforeTime = os.getenv('ICBC_EXPECT_BEFORETIME')
examClass = str(os.getenv('ICBC_EXAMCLASS'))

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

locations = [
    {"name": "Surrey Driver Licensing", "aPosID": 11},
    {"name": "Surrey Claim Centre", "aPosID": 269},
    {"name": "Guildford Boardwalk", "aPosID": 281},
    {"name": "Newton Claim Centre", "aPosID": 271},
    {"name": "Langley Driver Licensing", "aPosID": 153},
    {"name": "Port Coquitlam Driver Licensing", "aPosID": 73},
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]

user_agent = random.choice(user_agents)  # Select a random user agent for this run

def getToken():
    login_url = "https://onlinebusiness.icbc.com/deas-api/v1/webLogin/webLogin"

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*'
    }

    payload = {
        "drvrLastName": lastName,
        "licenceNumber": licenceNumber,
        "keyword": keyword
    }

    response = requests.put(login_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return response.headers.get("Authorization", "")
    else:
        print(f"Error {response.status_code}: {response.text}")
    return ""

def getAppointments(token, location):
    appointment_url = "https://onlinebusiness.icbc.com/deas-api/v1/web/getAvailableAppointments"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token,
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
    }

    payload = {
        "aPosID": location["aPosID"],
        "examType": f"{examClass}-R-1",
        "examDate": expactAfterDate,
        "ignoreReserveTime": "false",
        "prfDaysOfWeek": "[0,1,2,3,4,5,6]",
        "prfPartsOfDay": "[0,1]",
        "lastName": lastName,
        "licenseNumber": licenceNumber
    }

    response = requests.post(appointment_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
    return []

def getAppointmentDate(appointment):
    return appointment["appointmentDt"]["date"]

def appointmentMatchRequirement(appointment):
    appointmentDate = getAppointmentDate(appointment)
    thatDate = datetime.strptime(appointmentDate, DATE_FORMAT)
    beforeDate = datetime.strptime(expactBeforeDate, DATE_FORMAT)

    appointmentTime = appointment["startTm"]
    thatTime = datetime.strptime(appointmentTime, TIME_FORMAT)
    afterTime = datetime.strptime(expactAfterTime, TIME_FORMAT)
    beforeTime = datetime.strptime(expactBeforeTime, TIME_FORMAT)

    return thatDate <= beforeDate and afterTime <= thatTime <= beforeTime

def saveAppointments(appointments):
    with open('appointments.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Location", "Date", "Time"])

        for location_name, location_appointments in appointments.items():
            for appointment in location_appointments:
                writer.writerow([location_name, appointment["date"], appointment["time"]])

if __name__ == "__main__":
    token = getToken()
    if not token:
        print("Failed to retrieve token")
        exit(1)

    all_appointments = {}
    for location in locations:
        print(f"Checking location: {location['name']}")  # Debugging message
        appointments = getAppointments(token, location)
        matched_appointments = []
        for appointment in appointments:
            if appointmentMatchRequirement(appointment):
                appointmentDate = getAppointmentDate(appointment)
                appointmentTime = appointment["startTm"]
                matched_appointments.append({"date": appointmentDate, "time": appointmentTime})
                print(f"Location: {location['name']}, Date: {appointmentDate}, Time: {appointmentTime}")
        all_appointments[location["name"]] = matched_appointments
        
        wait_time = random.uniform(15, 35)  # Varying wait time for each location
        print(f"Waiting for {wait_time:.2f} seconds before checking the next location...")  # Debugging message
        time.sleep(wait_time)

    saveAppointments(all_appointments)
    print("Appointments recorded in appointments.csv")
