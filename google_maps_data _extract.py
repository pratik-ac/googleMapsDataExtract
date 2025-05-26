import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the chromedriver executable
chromedriver_path = '/usr/local/bin/chromedriver'  # Update this path

# Set up Selenium WebDriver (example uses Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Load the web page
driver.get('https://www.google.com/maps/search/manufacturing+businesses+in+Dane+County,+Wisconsin,+USA/@44.7788269,-94.8523255,6z?entry=ttu')

# Function to scroll within the specific container
def scroll_in_container(driver):
    scroll_pause_time = 2
    container_selector = 'div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd'  # Update the CSS selector if needed

    container = driver.find_element(By.CSS_SELECTOR, container_selector)
    last_height = driver.execute_script("return arguments[0].scrollHeight", container)

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return arguments[0].scrollHeight", container)
        if new_height == last_height:
            break
        last_height = new_height

# Wait until the desired elements are loaded
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Nv2PK.tH5CWc.THOPZb'))
    WebDriverWait(driver, 10).until(element_present)
except Exception as e:
    print(f"Error: {e}")
    driver.quit()
    sys.exit()

# Scroll within the container to load more results
scroll_in_container(driver)

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

compMain = soup.select('div.Nv2PK.tH5CWc.THOPZb a.hfpxzc')
compDetails = soup.select('div.Nv2PK.tH5CWc.THOPZb')

with open('job.txt', 'w') as f:
    for main, details in zip(compMain, compDetails):
        f.write('Company Name: ')
        name_element = main.get('aria-label')
        if name_element:
            f.write(name_element)
        f.write('\n')

        f.write('Company Address: ')
        address_element = details.select_one('div.UaQhfb.fontBodyMedium > div:nth-child(4) > div:nth-child(1) > span:nth-child(2) > span:nth-child(2)')
        if address_element:
            f.write(address_element.get_text())
        else:
            f.write('None')
        f.write('\n')

        f.write('Company Contacts: ')
        contacts_element = details.select_one('div.UaQhfb.fontBodyMedium > div:nth-child(4) > div:nth-child(2) > span:nth-child(2) > span.UsdlK')
        if contacts_element:
            f.write(contacts_element.get_text())
        else:
            f.write('None')
        f.write('\n')

        f.write('Company Website: ')
        website_element = details.select_one('a.lcr4fd.S9kvJb')
        if website_element:
            f.write(website_element.get('href'))
        else:
            f.write('None')
        f.write('\n')
        f.write('\n')

# Quit the WebDriver
driver.quit()
