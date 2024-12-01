import argparse
import datetime
import logging
import os

import requests
from bs4 import BeautifulSoup


def get_default_year(months_delay=4) -> int:
    """
    Determine the default year for the current month.
    The months_delay parameter is used to
    determine the year for a number of months past the event.
    """
    today = datetime.datetime.today()
    if today.month <= months_delay:
        return today.year - 1
    return today.year


def parse_args_year_day():
    # Parse 1st positional argument for day, can only be 1 to 25 inclusive.
    # Optional kw argument --year or -y overrides the default year (this year).
    ap = argparse.ArgumentParser()
    msg = "The day of the month to download"
    day_params = {"type": int, "choices": range(1, 26), "help": msg}
    ap.add_argument("day", **day_params)
    yr = get_default_year()
    msg = f"The year to download from (default: {yr})"
    year_params = {"type": int, "default": yr, "help": msg}
    ap.add_argument("--year", "-y", **year_params)
    args = ap.parse_args()
    return args.year, args.day


def get_cookie_token(file=".token.txt") -> str:
    """
    Retrieve the session cookie token from a file.

    Args:
        file: The path to the token file. Defaults to '.token.txt'.

    Returns:
        The session token as a string.

    Raises:
        FileNotFoundError: If the token file does not exist.
        Exception: For other I/O related errors.
    """
    if file.startswith("/"):
        path = file
    else:
        path = os.path.join(get_script_dir(), file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            token = f.read().strip()
            if not token:
                raise ValueError("Token file is empty.")
            return token
    except FileNotFoundError:
        raise FileNotFoundError(f"Token file not found at path: {path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the token file: {e}") from e


def download_advent_of_code_html(year, day):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {"session": get_cookie_token()}
    uagent_tag = "AdventOfCodeDownloader/1.0"
    uagent = f"{uagent_tag} (+https://github.com/marcus-grant/advent-of-code)"
    headers = {"User-Agent": uagent}
    response = requests.get(url, cookies=cookies, headers=headers)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful

    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find("main")
    if not main_content:
        raise ValueError("No main content tag found in the response.")

    return str(main_content)


def get_script_dir() -> str:
    """
    Return the directory where the current script is located.

    Returns:
        The absolute path to the script's directory.
    """
    return os.path.dirname(os.path.realpath(__file__))


# TODO: Ensure this works, otherwise keep fixme
# notfixme: Later this will be a repo of years bring this back, then
# def save_html(html_content, year, day):
def save_html(html_content: str, day: int):
    """
    Save the HTML content to a file within a day-specific directory.

    Args:
        html_content: The HTML content to save.
        day: The day of the month (1-25).

    Raises:
        IOError: If writing to the file fails.
    """
    day_dir = os.path.join(get_script_dir(), f"{day:02d}")
    os.makedirs(day_dir, exist_ok=True)
    file_path = os.path.join(day_dir, f"day{day:02d}.html")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info(f"Saved HTML content to {file_path}")
    except Exception as e:
        logging.error(f"Failed to write HTML content to {file_path}: {e}")
        raise IOError(f"Failed to write HTML content to {file_path}: {e}") from e


# Configure logging at the top of the script
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    try:
        year, day = parse_args_year_day()
        logging.info(f"Downloading AoC {year} Day {day}...")
        html_content = download_advent_of_code_html(year, day)
        save_html(html_content, day)
        logging.info(f"Successfully saved Day {day:02d} content.")
    except Exception as e:
        logging.error(e)
        exit(1)
