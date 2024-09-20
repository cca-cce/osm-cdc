# screenshot.py

from playwright.sync_api import sync_playwright

def take_full_page_screenshot(url, output_path):
    with sync_playwright() as p:
        # Launch the browser (Chromium in headless mode)
        browser = p.chromium.launch()
        page = browser.new_page()
        # Navigate to the specified URL
        page.goto(url)
        # Wait until the page is fully loaded
        page.wait_for_load_state('networkidle')
        # Take a full-page screenshot
        page.screenshot(path=output_path, full_page=True)
        # Close the browser
        browser.close()

# Usage example
if __name__ == "__main__":
    url = 'https://www.example.com'  # Replace with your target URL
    output_path = 'full_screenshot.png'  # Output file path
    take_full_page_screenshot(url, output_path)
    print(f"Screenshot saved to {output_path}")
    





