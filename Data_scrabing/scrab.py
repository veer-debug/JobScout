from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import numpy as np
import time
from data_base import Data
import pandas as pd
database=Data()


class WebScraper:
    def classify_job_by_keywords(job_title):
        # Expanded keyword lists for each category
        tech_keywords = [
            'engineer', 'developer', 'data scientist', 'it support', 'system administrator',
            'software engineer', 'network administrator', 'cloud engineer', 'devops', 'cybersecurity', 'backend', 'frontend',
            'full stack', 'qa engineer', 'data analyst', 'ai engineer', 'machine learning', 'database administrator', 'tech lead'
        ]
        
        graphic_keywords = [
            'graphic designer', 'ui/ux designer', 'illustrator', 'visual designer', 'web designer',
            'motion designer', '3d artist', 'layout designer', 'creative director', 'animator', 'art director',
            'digital artist', 'visual effects', 'concept artist', 'game designer'
        ]
        
        digital_keywords = [
            'seo specialist', 'content writer', 'social media manager', 'digital marketer', 'email marketing',
            'seo expert', 'online marketing', 'social media strategist', 'content strategist', 'ppc specialist', 'adwords',
            'affiliate marketer', 'e-commerce manager', 'growth hacker', 'brand manager', 'influencer marketing'
        ]

        # Normalize the job title to lowercase
        job_title = job_title.lower()

        # Check if the job title contains any keywords from each category
        if any(keyword in job_title for keyword in tech_keywords):
            return 'Technical'
        elif any(keyword in job_title for keyword in graphic_keywords):
            return 'Graphic Design'
        elif any(keyword in job_title for keyword in digital_keywords):
            return 'Digital Marketing'
        else:
            return 'Unknown'

        


    def extract_job_data(html_content, divs):
        """
        Extracts job data (titles, descriptions, locations) based on the outer div class.
        Returns a dictionary with the extracted data.
        """
        outer_div = BeautifulSoup(html_content, 'html.parser')
        
        # Find the outer div using the provided class name
        # outer_div = soup.find('div', class_=out_div)
        # Initialize dictionaries to hold extracted data
        job_data = {
            'job_titles': [],
            'job_location': [],
            'job_company': [],
            'job_url': [],
            'job_type':[],
        }
#         out_div=[[row['Outer_div'],row['Outer_div_tag']],row['If Dynamic_xpa']]
# divs=[[row['Name_div_tag'],roe['Name_div']],[row['Location_div_tag'],roe['Location_div']],[roe['Url_div_tag'],row['Url_div']],row['Name']]
        # Extract job titles 
        job_title_element = outer_div.find(divs[0][0], class_=divs[0][1])  
        if job_title_element:
            job_data['job_titles'].append(job_title_element.get_text(strip=True))
        else:
            job_data['job_titles'].append(np.nan)
        
        # Extract job Location 
        location_element = outer_div.find(divs[1][0], class_=divs[1][1])  
        if location_element:
            job_data['job_location'].append(location_element.get_text(strip=True))
        else:
            job_data['job_location'].append(np.nan)
        
        # Extract job URL 
        if divs[2][0] !='0':
            url_element = outer_div.find(divs[2][0], class_=divs[2][1])  
            if url_element and url_element.get('href'):  # Check if href exists
                job_data['job_url'].append(url_element.get('href'))
            else:
                job_data['job_url'].append(np.nan)
        else:
            job_data['job_url'].append(divs[2][1])


        # Extract job company 
        company_element = divs[3] 
        if company_element:
            job_data['job_company'].append(company_element.get_text(strip=True))
        else:
            job_data['job_company'].append(np.nan)
            
        # Extract job job Type 
        type_element = WebScraper.classify_job_by_keywords(job_data['job_titles'][0])
        if type_element:
            job_data['job_type'].append(type_element.get_text(strip=True))
        else:
            job_data['job_type'].append(np.nan)

        return job_data

    # Main function to process the html_data_list
    @staticmethod
    def process_html_data(html_data_list,divs):
        all_job_data = {
            'job_company': [],
            'job_titles': [],
            'job_location': [],
            'job_url': [],
            'job_type':[],
        }
        
        for html_content in html_data_list:
            job_data = WebScraper.extract_job_data(html_content)
            
            # Append to the main lists
            all_job_data['job_titles'].extend(job_data['job_titles'])
            all_job_data['job_location'].extend(job_data['job_location'])
            all_job_data['job_company'].extend(job_data['job_company'])
            all_job_data['job_url'].extend(job_data['job_url'])
            all_job_data['job_type'].extend(job_data['job_type'])
        df=pd.DataFrame(all_job_data)
        database.add_to_table(df)

    @staticmethod
    def scrape_job_data_static(url, out_div, divs):
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
                outer_div = driver.find_element(By.CLASS_NAME, out_div[0])
                html_content = outer_div.get_attribute('outerHTML')
                html_data_list.extend(html_content)
                print(f"HTML Content from Page {i + 1}:")
                print(html_content)

                # Find and click the link to navigate to the next page
                link = driver.find_element(By.CLASS_NAME, out_div[1])
                if link:link.click()
                else:return html_data_list
                print(f"Navigated to Page {i + 1}")
                print()
            except Exception as e:
                print(f"Error on page {i + 1}: {e}")
                break

        driver.quit()  # Close the browser after scraping
        WebScraper.process_html_data(html_data_list,divs)

    
