#
# Copyright Matt Holmes https://github.com/mjholmes
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from trend import TrendScraper
from prettytable import PrettyTable
import requests
import json
from dotenv import load_dotenv
import os


def post_to_teams(trend_url, title, message):
    headers = {"Content-Type": "application/json"}
    payload = {"title": title, "text": f"```\n{message}\n```"}
    response = requests.post(trend_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Message posted successfully")
    else:
        print(f"Failed to post message: {response.status_code}, {response.text}")


# Load environment variables from a .env file
load_dotenv(".env")

# Example usage
ip_addresses = os.getenv("IP_ADDRESSES")
username = os.getenv("BMSUSER")
password = os.getenv("BMSPASS")
webhook_url = os.getenv("WEBHOOK_URL")

# Validate the variables exist
if not ip_addresses or not username or not password or not webhook_url:
    print("Error: Missing required environment variables.")
    exit(1)

ip_addresses = ip_addresses.split(",")

exclude_labels = [
    "Solar Electric Immersion Heate",
]  # Define the labels to exclude


for ip in ip_addresses:
    print(f"Fetching alarm data for IP: {ip}")
    scraper = TrendScraper(ip, username, password)
    scraper.create_session()
    recent_alarms = scraper.get_recent_alarms(exclude_labels=exclude_labels)

    if recent_alarms:
        table = PrettyTable()
        table.field_names = recent_alarms[0].keys()
        for alarm in recent_alarms:
            table.add_row(alarm.values())
        table_str = table.get_string()
        print(table_str)

        # Send the table to Microsoft Teams
        title = f"Recent Alarms for IP {ip}"
        post_to_teams(webhook_url, title, table_str)

    # Logout regardless of if alarms were found
    scraper.logout()
