from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

class WebScraper:
    @staticmethod
    def classify_job_by_keywords(job_title):
        """
        Classifies a job based on keywords in the job title.
        Returns a job type as a string.
        """
        job_title = job_title.lower() if isinstance(job_title, str) else ""
        
        if "engineer" in job_title:
            return "Engineering"
        elif "developer" in job_title:
            return "Development"
        elif "manager" in job_title:
            return "Management"
        elif "designer" in job_title:
            return "Design"
        else:
            return "Other"

    @staticmethod
    def extract_job_data(html_content, divs):
        print(divs)
        # outer_div = BeautifulSoup(html_content, 'html.parser')
        outer_div=html_content
        job_data = {
            'job_titles': [],
            'job_location': [],
            'job_company': [],
            'job_url': [],
            'job_type': [],
        }

        # Extract job title
        job_title_element = outer_div.find(divs[0][0].strip(), class_=divs[0][1].strip())
        if job_title_element:
            job_data['job_titles'].append(job_title_element.get_text(strip=True))
        else:
            job_data['job_titles'].append(np.nan)

        # Extract job location
        location_element = outer_div.find(divs[1][0].strip(), class_=divs[1][1].strip())
        if location_element:
            job_data['job_location'].append(location_element.get_text(strip=True))
        else:
            job_data['job_location'].append(np.nan)

        # Extract job URL
        if divs[2][0] != '0':
            url_element = outer_div.find(divs[2][0].strip(), class_=divs[2][1].strip())
            if url_element and url_element.get('href'):  # Check if href exists
                job_data['job_url'].append(url_element.get('href'))
            else:
                job_data['job_url'].append(np.nan)
        else:
            job_data['job_url'].append(divs[2][1].strip())

        # Extract job company
        company_element = divs[3].strip()
        if isinstance(company_element, str):
            job_data['job_company'].append(company_element)
        elif company_element:
            job_data['job_company'].append(company_element.get_text(strip=True))
        else:
            job_data['job_company'].append(np.nan)

        # Classify job type based on title keywords
        job_type = WebScraper.classify_job_by_keywords(job_data['job_titles'][0])
        job_data['job_type'].append(job_type)

        return job_data

    @staticmethod
    def process_html_data(html_data_list, divs):
        # print(divs)
        all_job_data = {
            'job_company': [],
            'job_titles': [],
            'job_location': [],
            'job_url': [],
            'job_type': [],
        }
        
        for html_content in html_data_list:
            job_data = WebScraper.extract_job_data(html_content, divs)
            
            # Append to the main lists
            all_job_data['job_titles'].extend(job_data['job_titles'])
            all_job_data['job_location'].extend(job_data['job_location'])
            all_job_data['job_company'].extend(job_data['job_company'])
            all_job_data['job_url'].extend(job_data['job_url'])
            all_job_data['job_type'].extend(job_data['job_type'])
        
        df = pd.DataFrame(all_job_data)
        print(df)
        df.to_csv('Data.csv')

    @staticmethod
    def scrape_job_data_static(url, out_div, divs):
        print(out_div[0])
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        html_data_list = []
        driver.get(url)
        
        for i in range(5):
            time.sleep(10)
            try:
                html=driver.page_source
                with open('veer.html','w',encoding='utf-8') as f:
                    f.write(html)
                soup = BeautifulSoup(html, 'html.parser')
                # Find all elements with the specific class
                
                elements = soup.find_all(class_=out_div[0].strip())
                for i in elements:
                    html_data_list.append(i)
                print(len(html_data_list))
                # Navigate to the next page if applicable
                if out_div[1] != 0:
                    print('i am there')
                    
                    link = driver.find_element(By.CLASS_NAME, out_div[1])
                    if link:
                        link.click()
                else:
                    break
                
                print(f"Navigated to Page {i + 1}")
            except Exception as e:
                print(f"Error on page {i + 1}: {e}")
                break

        driver.quit()
        WebScraper.process_html_data(html_data_list, divs)
# WebScraper.scrape_job_data_static('https://olacareers.turbohire.co/dashboardv2?orgId=e0c1eb37-eb7a-4ca4-bcc5-d59ce4ce9212&type=0',['job-card-wrapper',0],[])