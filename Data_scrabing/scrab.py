from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from data_base import Data

db=Data()

class WebScraper:
    @staticmethod
    def classify_job_type(job_title):
        """
        Classify job type based on job title keywords.
        """
        if not job_title or pd.isna(job_title):
            return "Unknown"
        title = job_title.lower()
        if any(keyword in title for keyword in ['developer', 'engineer', 'programmer', 'data', 'software', 'tech']):
            return "Tech"
        elif any(keyword in title for keyword in ['designer', 'ui', 'ux', 'graphic', 'artist']):
            return "Design"
        elif any(keyword in title for keyword in ['marketing', 'sales', 'advertising', 'seo']):
            return "Marketing"
        else:
            return "Other"

    @staticmethod
    def extract_job_data(html_content, divs, url):
        """
        Extract job details using dynamic tags and attributes.
        """
        soup = html_content
        job_data = {
            'job_titles': [],
            'job_location': [],
            'job_url': [],
            'job_company': [],
        }

        # Extract job title
        title_tag, title_attr_key, title_attr_value = divs[0]
        title_element = soup.find(title_tag, {title_attr_key: title_attr_value})
        job_data['job_titles'].append(title_element.text.strip() if title_element else np.nan)

        # Extract job URL
        link_tag, link_attr_key, link_attr_value = divs[1]
        link_element = soup.find(link_tag, {link_attr_key: link_attr_value})
        if divs[3] == 'orient technologies':
            job_data['job_url'].append(url)
        else:
            job_data['job_url'].append(link_element['href'] if link_element and link_element.get('href') else url)

        # Extract job location
        location_tag, location_attr_key, location_attr_value = divs[2]
        location_element = soup.find(location_tag, {location_attr_key: location_attr_value})
        job_data['job_location'].append(location_element.text.strip() if location_element else np.nan)

        # Add company name
        job_data['job_company'].append(divs[3])

        return job_data

    @staticmethod
    def process_html_data(html_data_list, divs, url):
        all_job_data = {
            'job_company': [],
            'job_titles': [],
            'job_location': [],
            'job_url': [],
            'job_type': [],  # New field for job type
        }

        for html_content in html_data_list:
            job_data = WebScraper.extract_job_data(html_content, divs, url)

            all_job_data['job_titles'].extend(job_data['job_titles'])
            all_job_data['job_location'].extend(job_data['job_location'])
            all_job_data['job_company'].extend(job_data['job_company'])
            all_job_data['job_url'].extend(job_data['job_url'])
            
            # Add job type classification
            all_job_data['job_type'].extend(
                WebScraper.classify_job_type(title) for title in job_data['job_titles']
            )

        # Save to CSV
        df = pd.DataFrame(all_job_data)
        df.to_csv('Data.csv', index=False)
        print("Data saved to Data.csv")
        db.add_to_table(df)

    @staticmethod
    def scrape_job_data_static(url, out_div, divs):
        """
        Scrape static job data from the given URL.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        html_data_list = []
        driver.get(url)

        for _ in range(5):  # Max 5 pages
            time.sleep(5)
            try:
                # Parse the current page
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all job containers
                elements = soup.find_all(class_=out_div[0])
                html_data_list.extend(elements)

                # Navigate to the next page if applicable
                if out_div[1]:  # Check for pagination class or XPath
                    next_button = driver.find_element(By.CLASS_NAME, out_div[1])
                    next_button.click()
                else:
                    break
            except Exception as e:
                print(f"Error while scraping: {e}")
                break

        driver.quit()
        WebScraper.process_html_data(html_data_list, divs, url)
