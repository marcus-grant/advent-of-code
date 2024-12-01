import argparse
import datetime
import os
import requests
from bs4 import BeautifulSoup

def parse_args_year_day():
    # Parse 1st positional argument for day, can only be 1 to 25 inclusive.
    # Optional kw argument --year or -y overrides the default year (this year).
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "day",
        type=int,
        choices=range(1, 26),
        help="The day of the month to download")
    ap.add_argument(
        "--year", "-y",
        type=int,
        default=0, # Gets evaluated to false, then replaced with current year
        help="The year to download from")
    args = ap.parse_args()
    year = args.year if args.year else datetime.datetime.today().year
    return year, args.day

def get_cookie_token(file=".token.txt"):
    # First check if there's a directory '/' prefixed to the file name
    # If so, then the file is an absolute path, so use it as is
    # Otherwise, it's a relative path, so prepend the script's directory
    if file[0] == "/":
        path = file
    else:
        path = f"{get_script_dir()}/{file}"
    with open(path, "r") as f:
        return f.read().strip()

def download_advent_of_code_html(year, day):
    url = f"https://adventofcode.com/{year}/day/{day}"
    cookies = {'session': get_cookie_token()}
    response = requests.get(url, cookies=cookies)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful

    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find("main")

    return str(main_content)

def get_script_dir(): return os.path.dirname(os.path.realpath(__file__))

# FIXME: Later this will be a repo of years bring this back, then
# def save_html(html_content, year, day):
def save_html(html_content, day):
    with open(f"{get_script_dir()}/{day:02d}/day{day:02d}.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    (year, day) = parse_args_year_day()
    html_content = download_advent_of_code_html(year, day)
    save_html(html_content, day)
