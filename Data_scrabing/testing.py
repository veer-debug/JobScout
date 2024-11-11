from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def scrape_job_data_static(url, outer_div_class, link_class, company):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode if no GUI needed
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    html_data_list = []
    driver.get(url)
    for i in range(5):
        time.sleep(2)
        try:
            # Find the outer div using its class name
            outer_div = driver.find_element(By.CLASS_NAME, outer_div_class)
            html_content = outer_div.get_attribute('outerHTML')
            html_data_list.append(html_content)
            print(f"HTML Content from Page {i + 1}:")
            print(html_content)

            # Find and click the link to navigate to the next page
            link = driver.find_element(By.CLASS_NAME, link_class)
            if link:link.click()
            else:return html_data_list
            print(f"Navigated to Page {i + 1}")
            print()
        except Exception as e:
            print(f"Error on page {i + 1}: {e}")
            break

    driver.quit()  # Close the browser after scraping
    return html_data_list


# Example usage:
link = 'https://livspace.sensehq.com/careers'
outer_div_class = 'css-1tk7xz5'  # Update with the actual outer div class name
link_class = 'chakra-link'  # Update with the actual link class name
company = 'veer'

html_data = scrape_job_data_static(link, outer_div_class, link_class, company)
