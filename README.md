# Web Scraping and Notification System

## Project Overview

This project demonstrates a robust web scraping and notification system, showcasing skills in Python programming, data extraction, database management, and automated email notifications.

## Key Features

- **Web Scraping**: Utilizes `requests` and `selectorlib` to efficiently scrape tour information from a target website.
- **Data Extraction**: Implements custom extraction logic to parse relevant data from HTML content.
- **Database Integration**: Employs SQLite for persistent storage of scraped data, preventing duplicate entries.
- **Email Notifications**: Automatically sends email alerts for newly discovered tour information using SMTP.
- **Environment Variable Management**: Uses `python-dotenv` for secure handling of sensitive information.
- **Continuous Operation**: Runs in a loop, constantly checking for updates and new information.

## Technologies Used

- Python
- SQLite
- Libraries: requests, selectorlib, smtplib, sqlite3, dotenv

## Code Structure

The main script is organized into several key functions:

- `scrape()`: Retrieves HTML content from the target URL.
- `extract()`: Parses the HTML to extract relevant tour information.
- `store()`: Saves new tour data to the SQLite database.
- `read()`: Checks if tour data already exists in the database.
- `send_email()`: Dispatches email notifications for new tour information.

## Skills Demonstrated

- Web scraping and data extraction
- Database design and management
- Email automation
- Error handling and logging
- Environment variable usage for configuration
- Modular code organization

This project showcases my ability to create efficient, automated systems that can gather, process, and respond to data in real-time, skills that are valuable in many software development roles.