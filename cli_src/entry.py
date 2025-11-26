import argparse
import sys
import time

from cli_src.runTranslations import runTranslations  # Import your core logic


def simple_loader(duration=0.5, message="Processing..."):
    """Displays a simple, brief spinner/loader on the console."""
    # List of characters for the spinner animation
    spinner = ['|', '/', '-', '\\']

    # Calculate the end time
    end_time = time.time() + duration

    # Loop until the end time is reached
    while time.time() < end_time:
        # Iterate through the spinner characters
        for char in spinner:
            # Print the spinner character and the message
            # \r (carriage return) moves the cursor to the start of the line
            sys.stdout.write(f'\r{message} {char}')
            # Flush output buffer to make the update visible immediately
            sys.stdout.flush()
            # Wait a short moment
            time.sleep(0.1)

    # Clear the spinner line once done
    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
    sys.stdout.flush()

def run_translations():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        type=str,
        help="The path to the directory containing files to translate."
    )
    args = parser.parse_args()
    directory_path = args.path

    print(f"Running translations for directory: **{directory_path}**")
    simple_loader(duration=2.0, message="Analyzing files and preparing translations  ")
    runTranslations(directory_path)
