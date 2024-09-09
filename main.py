import requests
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants for the web scraping target URL and HTTP headers
URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

# Establish a connection to the SQLite database and create a cursor
connection = sqlite3.connect("data.db")


def scrape(url):
    """
    Scrapes the page source from the given URL.

    Args:
        url (str): The URL of the page to scrape.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    """
    Extracts specific information (tours) from the provided HTML source using SelectorLib.

    Args:
        source (str): The HTML content of the page.

    Returns:
        str: Extracted information from the page content.
    """
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    """
    Sends an email with the specified message using an SMTP server.

    Args:
        message (str): The content of the email to be sent.
    """
    host = "smtp.gmail.com"
    port = 465

    # Retrieve email credentials and receiver email from environment variables
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("PASSWORD")
    receiver = os.getenv("RECEIVER_EMAIL")
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    # print("Email was sent!")


def store(extracted):
    """
    Stores the extracted tour information in the SQLite database.

    Args:
        extracted (str): The tour information in a comma-separated string format.
    """
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?, ?, ?)", row)
    connection.commit()


def read(extracted):
    """
    Checks if the extracted tour information already exists in the SQLite database.

    Args:
        extracted (str): The tour information in a comma-separated string format.

    Returns:
        list: List of rows that match the extracted data in the database.
    """
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    try:
        # Ensure the events table exists
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS events
                             (band TEXT, city TEXT, date TEXT)''')
        connection.commit()

        # Main loop to continuously scrape, extract, store, and send email notifications
        while True:
            try:
                # Step 1: Scrape the URL for content
                scraped = scrape(URL)
                # Step 2: Extract the relevant information from the scraped content
                extracted = extract(scraped)
                print(f"Extracted data: {extracted}")

                if extracted != "No upcoming tours":
                    # Step 3: Check if the extracted information is already stored in the database
                    row = read(extracted)

                    # Step 4: If the information is new, store it and send an email notification
                    if not row:
                        store(extracted)
                        print("Sending email...")
                        send_email(message=f"""\
Subject: New email from Pythonprogrammer100

From: oladiporidwan10@gmail.com
{extracted}
""")
                    else:
                        print("Data already exists in database")
                else:
                    print("No upcoming tours")

                time.sleep(1)
            except Exception as e:
                print(f"An error occurred in the main loop: {str(e)}")
                time.sleep(5)  # Wait a bit longer before retrying
    except Exception as e:
        print(f"A critical error occurred: {str(e)}")
    finally:
        connection.close()