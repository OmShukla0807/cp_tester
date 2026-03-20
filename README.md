# CP Stress Tester & Scraper 🚀

A Python-based command-line tool designed to automate the testing of competitive programming solutions. It scrapes sample test cases directly from platforms like Codeforces and automatically checks local solutions against the expected outputs.

## Features
* **Automated Scraping:** Fetches sample inputs and outputs directly from problem URLs.
* **Local Execution:** Runs local C++ or Python solutions and feeds them the scraped inputs.
* **Strict Judging:** Compares your output against the expected output and provides immediate Pass/Fail feedback.

## Tech Stack
* Python 3
* `requests` & `BeautifulSoup4` (Web Scraping)
* `subprocess` (Code Execution)

## Setup & Usage

## Future Enhancements
* Support for multiple CP platforms.
* Auto-generation of folder structures for contests.