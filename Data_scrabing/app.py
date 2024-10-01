from flask import Flask, render_template, request, redirect, url_for
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

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


@app.route("/", methods=["GET", "POST"])
def scrape():
    if request.method == "POST":
        # Get form data
        url = request.form.get('url')
        outer_div_class = request.form.get('outer_div_class')
        page_type = request.form.get('page_type')  
        load_more_css = request.form.get('load_more_css')
        next_page_css = request.form.get('next_page_css')

        # Collect columns data
        columns = []
        column_index = 0
        while True:
            column_name = request.form.get(f'column_name_{column_index}')
            column_class = request.form.get(f'column_class_{column_index}')
            column_type = request.form.get(f'column_type_{column_index}')

            if not column_name:
                break  # Stop if no more columns
            columns.append({
                'name': column_name,
                'class': column_class,
                'type': column_type
            })
            column_index += 1

        # Initialize the WebScraper
        scraper = WebScraper()
        scraped_data = []
        page_type="static"

        # Call the appropriate scraper based on page type
        if page_type == "infinite_scroll":
            scraped_data = scraper.infinite_scroll(url, outer_div_class, columns)
        elif page_type == "dynamic":
            scraped_data = scraper.dynamic_webpage(url, load_more_css, next_page_css, outer_div_class, columns)
        elif page_type == "static":
            scraped_data = scraper.static_page(url, outer_div_class, columns)

        # Close the scraper
        scraper.close()

        # Write the scraped data to a CSV file
        with open("scraped_data.csv", mode="w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=[col['name'] for col in columns])
            writer.writeheader()
            writer.writerows(scraped_data)

        # Redirect to a download page or a success page
        return redirect(url_for("success"))

    return render_template("index.html")


@app.route("/success")
def success():
    return "Data successfully scraped and saved to scraped_data.csv!"


if __name__ == "__main__":
    app.run(debug=True)
