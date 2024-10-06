# ICBC Appointment Bot

Robot for checking ICBC road test appointments.

### Usage

Make sure the .env file is properly configured with your ICBC and Gmail credentials.
To start scraping for ICBC appointments, run checker_bot.py. This script will automatically check for appointments every few minutes and send an email if earlier slots are found.
Execute the following command to run the bot:
```python
python checker_bot.py
```
## Config

create a .env file in the root directory to store your configuration values, such as ICBC credentials and Gmail details. `./.env`
```yaml
# .env file
ICBC_LASTNAME="YOUR_LAST_NAME"
ICBC_LICENCENUMBER="YOUR_LICENCE_NUMBER"
ICBC_KEYWORD="KEYWORD"
ICBC_EXPECT_AFTERDATE="2024-07-13"  # YYYY-MM-DD
ICBC_EXPECT_BEFOREDATE="2024-08-31"  # YYYY-MM-DD
ICBC_EXPECT_AFTERTIME="07:00"  # HH:MM
ICBC_EXPECT_BEFORETIME="17:30"  # HH:MM
ICBC_EXAMCLASS=7  # 5/7

GMAIL_SENDER_ADDRESS="SENDER_EMAIL@gmail.com"
GMAIL_SENDER_PASS="YOUR_EMAIL_PASSWORD"
GMAIL_RECEIVER_ADDRESS="RECEIVER_EMAIL@gmail.com"
```

## Usage

For now, it only support getting the appointments in **Point Grey**
```python
point_grey = {
    "aPosID": 9,
    "examType": examClass+"-R-1",
    "examDate": expactAfterDate,
    "ignoreReserveTime": "false",
    "prfDaysOfWeek": "[0,1,2,3,4,5,6]",
    "prfPartsOfDay": "[0,1]",
    "lastName": lastName,
    "licenseNumber": licenceNumber
}
```
## Locations
| Location  | posID |
| ------------- | ------------- |
| Richmond claim centre (Elmbridge Way)  | 273  |
| Richmond driver licensing (Lansdowne Centre mall)  | 93  |
| Vancouver driver licensing (Point Grey)  | 9  |
| Vancouver claim centre (Kingsway)  | 275  |
| Burnaby claim centre (Wayburne Drive)  | 274  |
| Surrey driver licensing  | 11  |
| Newton claim centre (68 Avenue)  | 271  |
| Surrey claim centre (152A St.)  | 269  |
| North Vancouver driver licensing  | 8  |

## Contributing
Feel free to contribute.

1. Able to change location
2. Able to choose Day of week
