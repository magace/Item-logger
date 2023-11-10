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
    # If the application is run as a bundle (pyinstaller .exe)
    application_path = os.path.dirname(sys.executable)
elif __file__:
    # If the application is run from a python script (not bundled)
    application_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(application_path, "config.json"), "r") as config_file:
    config = json.load(config_file)

webhook_url = config["webhook_url"]
match_file = os.path.join(application_path, "match.txt")
use_match_file = config.get("useMatchFile", False)
clear_d2bot_errors = config.get("clearD2BotErrors", False)
error_x = config["errorX"]
error_y = config["errorY"]

def main():
    print("[blue]Discord Item Logger Loaded[/blue]")
    print("[blue]Match File Loaded[/blue]")
    print(f"[blue]Using match file: {use_match_file}[/blue]")
    print(f"[blue]Clearing D2BOT Errors: {clear_d2bot_errors} Clicking OK at {error_x} x {error_y}[/blue]")    
    while True:
        check_files()
        if clear_d2bot_errors:
            check_error_window(error_x, error_y)
        time.sleep(2)
def check_files():
    if use_match_file:
        prev_size = os.path.getsize(match_file)
    else:
        prev_size = None

    for img_path in config["img_paths"]:
        files = os.listdir(img_path)
        for file in files:
            file_path = os.path.join(img_path, file)
            if os.path.isfile(file_path):
                item_posted = read_text(file, img_path)
                if item_posted:
                    os.remove(file_path)
                    if use_match_file:
                        current_size = os.path.getsize(match_file)
                        if current_size != prev_size:
                            print(f"[blue]Match File Updated...[/blue]")
                            prev_size = current_size
def check_error_window(error_x, error_y):
    error_title = "An error has occured!"
    try:
        # Find the window with the error title
        error_window = gw.getWindowsWithTitle(error_title)
        if error_window:
            print(f"[bright_red]Error window found. Bringing to top and clicking 'OK' at {error_x} x {error_y}.[/bright_red]")
            # Bring the error window to the top
            error_window[0].activate()
            # Click the 'OK' button using pydirectinput at the specified coordinates
            pydirectinput.click(error_x, error_y, duration=0.5)
    except IndexError:
        # If the window with the error title is not found, IndexError will be raised
        pass

def read_text(file_name, img_path):
    current_time = datetime.datetime.now().strftime("%m/%d/%y %I:%M %p")
    if use_match_file:
        modified_file_name = os.path.splitext(file_name.lower())[0].replace(' ', '')
        with open(match_file, "r") as file:
            lines = [line.strip().lower().replace(' ', '') for line in file.readlines()]
        for line in lines:
            if line in modified_file_name:
                print(f"[bright_blue]{current_time} - Match found for: {file_name}[/bright_blue]")
                webhook(file_name, img_path)
                return True
    else:
        print(f"[cyan]{current_time} - Item Found: {file_name}[/cyan]") 
        webhook(file_name, img_path)
        return True
    return False

def webhook(file_to_send, img_path):
    file_path = os.path.join(img_path, file_to_send)
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]
    with open(file_path, "rb") as f:
        files = {"file": (filename, f, mime_type)}
        # Remove the file extension from the filename
        display_name = os.path.splitext(filename)[0]
        # Strip the 'Kept' prefix and numbers from the filename using regular expressions
        display_name = re.sub(r'^Kept\s+|\d+', '', display_name).strip()
        # Prepare the message with the file name and current date and time
        current_time = datetime.datetime.now().strftime("%m/%d/%y %I:%M %p")
        message = f"```\n{current_time} - {display_name}\n```"
        # Send the message along with the file as an attachment
        response = requests.post(webhook_url, data={"content": message}, files=files)
        print(f"[yellow]{current_time} - Discord Hook Sent: {display_name}[/yellow]")
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("Exception: ", e)
    