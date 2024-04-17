from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import threading

def setup_browser():
    options = webdriver.ChromeOptions()
    options.set_capability("pageLoadStrategy", "eager")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    return browser

def send_request_with_browser(browser, url):
    start_time = time.time()  # Capture start time
    browser.refresh()  # Refresh the page
    # Wait for a specific element that signifies that the page has loaded
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "header-image"))
    )
    end_time = time.time()  # Capture end time
    duration = end_time - start_time  # Calculate the duration
    print(f"Request to {url} took {duration} seconds.")

def refresh_at_target_time(target_time, browser, url):
    while True:
        now = datetime.now()
        if now >= target_time:
            print("Automatic refresh triggered at target time.")
            send_request_with_browser(browser, url)
            break
        time.sleep(1)  # Sleep to reduce the load on the processor

def main():
    browser = setup_browser()
    url = ""
    browser.get(url)  # Pre-load the page

    # Setup target time for automatic refresh
    target_time = datetime.now().replace(hour=11, minute=46, second=15, microsecond=0)
    if datetime.now() > target_time:
        target_time += timedelta(days=1)  # Set for the next day if time has passed today

    # Start a background thread to handle the timed refresh
    threading.Thread(target=refresh_at_target_time, args=(target_time, browser, url)).start()

    # Main loop for manual refresh
    try:
        while True:
            command = input("Press Enter to refresh the page manually or type 'exit' to quit: ")
            if command == '':
                send_request_with_browser(browser, url)
            elif command.lower() == 'exit':
                break
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
