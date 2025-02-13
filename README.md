# Trend Scraping

This repository contains a Python script `main.py` designed to scrape alarm data from a Trend system and post the results to a Microsoft Teams channel.

## Overview

The `main.py` script uses the `TrendScraper` class from `trend.py` to collect alarm data from a Trend system. It then formats the data into a table and posts it to a Microsoft Teams channel using a webhook URL.

## Usage

1. **Installation**: Ensure you have Python installed on your system. Clone this repository and navigate to the directory.

    ```bash
    git clone https://github.com/yourusername/trend-scraping.git
    cd trend-scraping
    ```

2. **Dependencies**: Install the required dependencies using pip.

    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables**: Create a `.env` file in the root directory of the project to store your environment variables. Below is an example:

    ```env
    IP_ADDRESSES=172.24.7.18,172.24.7.19
    BMSUSER=your_username
    BMSPASS=your_password
    WEBHOOK_URL=your_teams_webhook_url
    ```

    Replace the placeholder values with your actual IP addresses, username, password, and Teams webhook URL.

4. **Running the Script**: Execute the `main.py` script to start scraping alarm data and posting it to Microsoft Teams.

    ```bash
    python main.py
    ```

## Features

- Scrapes alarm data from a Trend system.
- Formats the data into a table.
- Posts the formatted data to a Microsoft Teams channel.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.

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