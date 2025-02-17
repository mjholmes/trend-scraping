# Trend Scraping

Trend (now Honeywell) IQ building and energy management systems are commonly found managing medium to large buildings. Unfortunatly as with many BEMS installations the systems are rarely setup and integrated in a way that offers a good user experience for building users.

This script is designed to scrape alarm data from an isolated and rather unloved Trend BEMS system and post the results to a Microsoft Teams channel giving remote Estates teams a level of offsite oversight. Ideally XML web services would be used to gather the data rather than web scraping but this was not licensed on the iQ3 on-site and not enabled on the iQ4s.

The script has been tested on an IQ3 XCITE running firmware version 3.07 and on some iQ4 series (iQ422) running firmware version 4.36.


## Overview

The script uses username/password authentication to grab an authentication token (`param0`) which is then used to access the main user web interface and scrape the required information using `beautifulsoup`.

## Usage

I'd typically set this up in a virtual environment and run it periodically from CRON.
By default the code is setup to run regularly every 4 hours. If you want to change the interval edit `main.py` and include the required interval in the call to `get_recent_alarms`.

1. **Installation**: Ensure you have Python installed on your system. Clone this repository and navigate to the directory.

   ```bash
   cd /opt
   sudo git clone https://github.com/mjholmes/trend-scraping.git
   cd trend-scraping
   ```

1. **Create a virutal env** to keep all the dependencies self-contained.

   ```bash
   python3 -m venv .
   source ./bin/activate
   ```

1. **Dependencies**: Install the required dependencies using pip.

   ```bash
   pip3 install -r requirements.txt
   ```

1. **Environment Variables**: Create a `.env` file in the root directory of the project to store your environment variables. Below is an example:

   ```env
   IP_ADDRESSES=192.168.0.10,192.168.0.11
   BMSUSER=your_username
   BMSPASS=your_password
   WEBHOOK_URL=your_teams_webhook_url
   ```

   Replace the placeholder values with your actual IP addresses, username, password, and Teams webhook URL (in Teams right click on a channel, choose "Manage channel" then "Settings" and add an "incoing webhook" connector).

1. **Running the Script**: Execute the `main.py` script to start scraping alarm data and posting it to Microsoft Teams.

   ```bash
   python3 main.py
   ```

1. **Create a CRON entry** to run the code reguarly. With virtual environments you can choose to call the python interpretter directly from the venv or wrtie a small shell script wrapper `scrape-trend.sh`:

   ```bash
   #!/bin/bash

   cd /opt/trend-scraping

   source ./bin/activate
   python3 main.py
   deactivate
   ```

   Add the crontab entry:
   ```bash
   0	*/4	*	*	*	/opt/trend-scraping/scrape-trend.sh
   ```


## License

This project is licensed under LGPL 3 or later.

## Methods

### `TrendScraper`

#### `create_session()`

Creates a session and logs in to the Trend system.

#### `fetch_alarm_data()`

Fetches the alarm data from the Trend system.

#### `get_recent_alarms(exclude_labels=None)`

Retrieves recent alarms, excluding specified labels.

#### `logout()`

Logs out from the Trend system.

### `post_to_teams(webhook_url, title, message)`

Posts a message to a Microsoft Teams channel using a webhook URL.
