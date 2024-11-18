import re
import os
import csv
from playwright.sync_api import sync_playwright

def sanitize_filename(url):
    # Replace one or more non-alphanumeric characters with a single dash
    return re.sub(r'[^a-zA-Z0-9]+', '-', url).strip('-')

def take_full_page_screenshot(url, output_path):
    with sync_playwright() as p:
        # Launch the browser (Chromium in headless mode)
        browser = p.chromium.launch()
        # Set a more natural user agent and viewport size
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        # Navigate to the specified URL
        page.goto(url, wait_until="domcontentloaded")

        # Simulate user actions to make the visit more natural
        page.mouse.move(100, 100)
        page.wait_for_timeout(1000)  # Wait for 1 second
        page.mouse.wheel(0, 500)  # Scroll down
        page.wait_for_timeout(1000)  # Wait for 1 second

        # Try to accept cookies if there's a common 'Accept' button
        try:
            page.locator("button:text('Accept')").click(timeout=5000)
        except:
            pass  # If the cookie banner isn't found, continue without clicking

        # Increase waiting time to ensure multimedia content has loaded
        page.wait_for_timeout(5000)  # Wait an additional 5 seconds
        page.wait_for_load_state('networkidle')

        # Take a full-page screenshot
        page.screenshot(path=output_path, full_page=True)
        # Close the browser
        browser.close()

if __name__ == "__main__":
    input_file = 'urls.tsv'  # TSV file containing URLs

    # Read URLs from TSV file
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
    else:
        with open(input_file, 'r', newline='') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                if row:
                    url = row[0].strip()
                    if url:
                        # Create a sanitized output filename
                        output_filename = sanitize_filename(url) + '.png'
                        try:
                            take_full_page_screenshot(url, output_filename)
                            print(f"Screenshot saved to {output_filename}")
                        except Exception as e:
                            print(f"Failed to take screenshot of {url}: {e}")
