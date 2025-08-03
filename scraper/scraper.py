import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
import asyncio
import re

# Set the event loop policy for Windows to support subprocesses
if os.name == 'nt':  # nt indicates Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*%]', '_', filename)

def scrape_content_and_screenshot(url, screenshot_path="screenshots"):
    try:
        # Ensure the screenshot directory exists
        os.makedirs(screenshot_path, exist_ok=True)

        # Send HTTP request with a user-agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'id': 'mw-content-text'}).get_text(strip=True) if soup.find('div', {'id': 'mw-content-text'}) else soup.get_text(strip=True)

        sanitized_filename = sanitize_filename(os.path.basename(url))
        screenshot_file = os.path.join(screenshot_path, f"{sanitized_filename}.png")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Set similar headers in Playwright
            page.set_extra_http_headers(headers)
            page.goto(url)
            page.screenshot(path=screenshot_file)
            browser.close()

        return content, screenshot_file

    except Exception as e:
        print(f"Error scraping content or taking screenshot: {e}")
        return None, None