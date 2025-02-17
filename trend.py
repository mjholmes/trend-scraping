#
# Copyright Matt Holmes https://github.com/mjholmes
# SPDX-License-Identifier: LGPL-3.0-or-later
#

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class TrendScraper:
    """
    A class to scrape alarm data from a Trend BEMS controller.

    Attributes:
        ip_address (str): The IP address of the Trend controller.
        username (str): The username for authentication.
        password (str): The password for authentication.
        session (requests.Session): The session object to persist the login.
        param_value (str): The extracted param0 value from the redirection URL (used as a session token).

    Methods:
        create_session(): Creates a session and logs in to the Trend system.
        fetch_alarm_data(): Fetches the alarm data from the Trend system.
        get_recent_alarms(exclude_labels=None, hours=4): Retrieves recent alarms, excluding specified labels.
        logout(): Logs out from the Trend system.
    """

    def __init__(self, ip_address, username, password):
        """
        Initializes the TrendScraper with the given IP address, username, and password.

        Args:
            ip_address (str): The IP address of the Trend controller.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.session = None
        self.param_value = None

    def create_session(self):
        """
        Creates a session and logs in to the Trend controller.

        Raises:
            requests.RequestException: If the session creation fails.
        """
        try:
            # URL for the login form
            login_url = f"http://{self.ip_address}/beginsession"

            # Payload with login credentials
            payload = {
                "ServerCommand": "beginsession",
                "ModuleFullName": "",
                "param1": self.username,
                "param2": self.password,
                "param-1": "TRUE",
            }

            # Headers to specify the content type
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            # Create a session to persist the login
            self.session = requests.Session()

            # Post the login form
            response = self.session.post(login_url, data=payload, headers=headers)
            response.raise_for_status()

            # Extract the 'Trend963Redirection' header
            redirection_url = response.headers.get("Trend963Redirection")
            if redirection_url:
                # Find the position of 'param0=' in the URL
                param_pos = redirection_url.find("param0=")
                if param_pos != -1:
                    # Extract the string after 'param0='
                    self.param_value = redirection_url[param_pos + len("param0=") :]
                    print("Extracted param0 value:", self.param_value)
                else:
                    print("param0 not found in redirection URL")
            else:
                print("Trend963Redirection header not found")
        except requests.RequestException as e:
            print(f"Failed to create session: {e}")

    def fetch_alarm_data(self):
        """
        Fetches the alarm data from the Trend system.

        Returns:
            list: A list of dictionaries containing the alarm data.
        """
        if not self.param_value:
            print("param0 value not found")
            return []

        try:
            # Construct the new URL with the extracted param0 value
            new_url = f"http://{self.ip_address}/alarms.htm?param0={self.param_value}"

            # Send a GET request to the new URL
            new_response = self.session.get(new_url)
            new_response.raise_for_status()

            # Parse the HTML content from the new response
            soup = BeautifulSoup(new_response.text, 'html.parser')
            table = soup.find('table', cellpadding="5")
            if table:
                headers = [header.text for header in table.find_all('td', class_='heading')]
                rows = []
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td', class_='data')
                    row_data = {headers[i]: cells[i].text for i in range(len(cells))}
                    rows.append(row_data)
                
                return rows
            else:
                print("No table found in the response")
                return []
        except requests.RequestException as e:
            print(f"Failed to fetch alarm data: {e}")
            return []

    def get_recent_alarms(self, exclude_labels=None, hours=4):
        """
        Retrieves recent alarms, excluding specified labels.

        Args:
            exclude_labels (list): A list of labels to exclude from the results.
            hours (int): The number of hours to look back for recent alarms.

        Returns:
            list: A list of dictionaries containing the recent alarm data.
        """
        exclude_labels = exclude_labels or []
        alarms = self.fetch_alarm_data()
        recent_alarms = []

        current_time = datetime.now()
        time_period_ago = current_time - timedelta(hours=hours)

        for alarm in alarms:
            row_time = datetime.strptime(alarm['Time'], '%b %d %Y %H:%M:%S')
            if row_time > time_period_ago and alarm['Module Label'] not in exclude_labels:
                recent_alarms.append(alarm)

        return recent_alarms

    def logout(self):
        """
        Logs out from the Trend system.
        """
        if self.session:
            logout_url = f"http://{self.ip_address}/logout.htm?param0={self.param_value}"
            self.session.get(logout_url)
            self.session.close()
            print("Logged out successfully")