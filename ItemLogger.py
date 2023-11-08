import os
import time
import requests
import mimetypes
import sys
import pygetwindow as gw
import pydirectinput
import re
import datetime
from rich import print
import pygetwindow as gw
import pydirectinput
import json

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(application_path, "config.json"), "r") as config_file:
    config = json.load(config_file)

webhook_url = config["webhook_url"]
match_file = os.path.join(application_path, "match.txt")

def main():
    print("[blue]Discord Item Logger Loaded...[/blue]")
    print("[blue]Match File Loaded...[/blue]")
    while True:
        check_files()
        check_error_window()
        time.sleep(2)
def check_files():
    prev_size = os.path.getsize(match_file)
    for img_path in config["img_paths"]:
        files = os.listdir(img_path)
        for file in files:
            file_path = os.path.join(img_path, file)
            if os.path.isfile(file_path):
                read_text(file, img_path)  
                current_size = os.path.getsize(match_file)
                if current_size != prev_size:
                    print(f"[blue]Match File Loaded...[/blue]")
                    prev_size = current_size
                    with open(match_file, "r") as file:
                        lines = [line.strip().lower().replace(' ', '') for line in file.readlines()]
                os.remove(file_path)

def check_error_window():
    error_title = "An error has occured!"
    try:
        # Find the window with the error title.  You would probably need to change x y coords.
        error_window = gw.getWindowsWithTitle(error_title)
        if error_window:
            print("[bright_red]Error window found. Bringing to top and clicking 'OK'.[/bright_red]")
            error_window[0].activate()
            pydirectinput.click(1103, 595, duration=0.5)
    except IndexError:
        pass
def read_text(file_name, img_path):
    modified_file_name = os.path.splitext(file_name.lower())[0].replace(' ', '')
    current_time = datetime.datetime.now().strftime("%m/%d/%y %I:%M %p")
    with open(match_file, "r") as file:
        lines = [line.strip().lower().replace(' ', '') for line in file.readlines()]
    for line in lines:
        if line in modified_file_name:
            print(f"[bright_blue]{current_time} - Match found for: {file_name}[/bright_blue]")
            webhook(file_name, img_path)  # pass the original file name and img_path
            return True
    file_name_no_ext = os.path.splitext(file_name)[0]  # Remove the extension
    file_name_no_numbers = re.sub(r'\d', '', file_name_no_ext)  # Remove the numbers
    print(f"[cyan]{current_time} - Item Found: {file_name_no_numbers}[/cyan]")     
    return False
def webhook(file_to_send, img_path):
    file_path = os.path.join(img_path, file_to_send)
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]
    with open(file_path, "rb") as f:
        files = {"file": (filename, f, mime_type)}
        display_name = os.path.splitext(filename)[0]
        display_name = re.sub(r'^Kept\s+|\d+', '', display_name).strip()
        current_time = datetime.datetime.now().strftime("%m/%d/%y %I:%M %p")
        message = f"```\n{current_time} - {display_name}\n```"
        response = requests.post(webhook_url, data={"content": message}, files=files)
        print(f"[yellow]{current_time} - Discord Hook Sent: {display_name}[/yellow]")
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("Exception: ", e)
