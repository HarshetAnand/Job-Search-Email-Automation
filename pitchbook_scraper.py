from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from dotenv import load_dotenv
import os

load_dotenv()

NETID = os.environ.get("UW_NETID")
NETID_PASSWORD = os.environ.get("UW_PASSWORD")
PITCHBOOK_EMAIL = os.environ.get("PITCHBOOK_EMAIL")
PITCHBOOK_PASSWORD = os.environ.get("PITCHBOOK_PASSWORD")

# Search results page
SEARCH_URL = "https://my-pitchbook-com.ezproxy.library.wisc.edu/search-results/s569449811/companies"

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

wait = WebDriverWait(driver, 1200)

emails = []

try:
    print("Opening UW Madison PitchBook splash page...")
    driver.get("https://uwisconsin-pitchbook-com.ezproxy.library.wisc.edu/")

    # Click the NetID Sign In link
    print("Waiting for NetID Sign In link...")
    netid_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'NetID Sign In')]"))
    )
    netid_link.click()
    print("✅ Clicked NetID Sign In link.")

    # Wait for NetID login fields
    print("Waiting for NetID login fields...")
    username_input = wait.until(EC.presence_of_element_located((By.ID, "j_username")))
    password_input = driver.find_element(By.ID, "j_password")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Log In')]")

    # Fill NetID credentials
    print("Entering NetID credentials...")
    username_input.send_keys(NETID)
    password_input.send_keys(NETID_PASSWORD)
    login_button.click()
    print("✅ NetID login submitted.")

    # Wait for PitchBook login form
    print("Waiting for PitchBook login form...")
    email_input = wait.until(EC.presence_of_element_located((By.ID, "login")))
    pitchbook_password_input = driver.find_element(By.ID, "password")
    pitchbook_login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Log in']")

    # Fill PitchBook credentials
    print("Entering PitchBook credentials...")
    email_input.send_keys(PITCHBOOK_EMAIL)
    pitchbook_password_input.send_keys(PITCHBOOK_PASSWORD)
    pitchbook_login_button.click()
    print("✅ PitchBook login submitted.")

    wait.until(EC.presence_of_element_located((By.XPATH, "//body")))

    # Close the welcome popup if it appears
    print("Waiting for potential welcome popup...")
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'close') and contains(@class, 'js-done')]"))
        )
        close_button.click()
        print("✅ Closed the welcome popup.")
    except Exception:
        print("ℹ️ No popup appeared.")

    # Go to search results page
    print("Navigating to search results...")
    driver.get(SEARCH_URL)

    page_num = 1

    while True:
        print(f"\n🟢 Processing page {page_num}...")

        # Wait for emails to load
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]"))
        )

        email_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
        print("Number of email links found on this page:", len(email_links))

        for el in email_links:
            email = el.get_attribute("href").replace("mailto:", "").strip()
            if email and email not in emails:
                print("✅ Found email:", email)
                emails.append(email)

        # Try to find Next button
        print("Looking for Next button...")
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to next page']")
            if not next_button.is_enabled():
                print("❌ Next button is disabled. Reached last page.")
                break
            else:
                print("✅ Clicking Next...")
                next_button.click()
                page_num += 1
                time.sleep(5)  # Wait for next page to load
        except Exception:
            print("❌ No Next button found. Reached last page.")
            break

    if emails:
        rows = []
        count = 0
        for email in emails:
            rows.append([email])
            count += 1
            if count % 97 == 0:
                rows.append([""])  # Insert empty row

        df = pd.DataFrame(rows, columns=["Email"])
        df.to_csv("pitchbook_emails.csv", index=False)
        print("\n✅ Done! Results saved to pitchbook_emails.csv with spacing every 97 rows.")
    else:
        print("\n⚠️ No emails found.")


except Exception as e:
    print("\n❌ An error occurred:", e)

finally:
    input("\n✅ Script completed. Press Enter to close the browser...")
    driver.quit()


