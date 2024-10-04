from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


class WebScraper:
    def __init__(self):
        # Set up Selenium WebDriver with ChromeDriverManager
        self.service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def infinite_scroll(self, url, outer_div_class, columns):
        """Scrape a page with infinite scrolling."""
        self.driver.get(url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Scroll down in a loop until no more new content is loaded
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Allow content to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height

        # Extract the page source and parse it
        page_source = self.driver.page_source
        return self._parse_page(page_source, outer_div_class, columns)

    def dynamic_webpage(self, url, load_more_css, next_page_css, outer_div_class, columns):
        """Scrape a dynamic webpage requiring interactions."""
        self.driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # If a "Load More" button exists, click it to load more content
        if load_more_css:
            try:
                load_more_button = self.driver.find_element(By.CSS_SELECTOR, load_more_css)
                load_more_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"Load More button not found: {e}")

        # Handle pagination
        if next_page_css:
            while True:
                try:
                    next_page_button = self.driver.find_element(By.CSS_SELECTOR, next_page_css)
                    next_page_button.click()
                    time.sleep(3)
                except Exception as e:
                    print(f"No Next Page button found or no more pages: {e}")
                    break

        # Extract the page source and parse it
        page_source = self.driver.page_source
        return self._parse_page(page_source, outer_div_class, columns)

    def static_page(self, url, outer_div_class, columns):
        """Scrape a static webpage."""
        self.driver.get(url)
        page_source = self.driver.page_source
        return self._parse_page(page_source, outer_div_class, columns)

    def _parse_page(self, page_source, outer_div_class, columns):
        """Helper function to parse the page and extract data based on provided structure."""
        soup = BeautifulSoup(page_source, 'html.parser')
        outer_divs = soup.find_all('div', class_=outer_div_class)

        scraped_data = []
        for outer_div in outer_divs:
            row_data = {}
            for column in columns:
                element = outer_div.find(column['type'], class_=column['class'])
                if element:
                    if column['type'] == 'a':
                        row_data[column['name']] = element.get('href')  # Extract href for links
                    else:
                        row_data[column['name']] = element.get_text().strip()  # Extract text
                else:
                    row_data[column['name']] = None
            scraped_data.append(row_data)

        return scraped_data

    def close(self):
        """Clean up and close the WebDriver."""
        self.driver.quit()
