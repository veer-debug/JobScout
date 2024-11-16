import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

# Optional: Set up logging to capture errors and debugging information
logging.basicConfig(level=logging.INFO)

class WebScraper:

    @staticmethod
    def classify_job_by_keywords(job_title):
        try:
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

            job_title = job_title.lower()

            if any(keyword in job_title for keyword in tech_keywords):
                return 'Technical'
            elif any(keyword in job_title for keyword in graphic_keywords):
                return 'Graphic Design'
            elif any(keyword in job_title for keyword in digital_keywords):
                return 'Digital Marketing'
            else:
                return 'Unknown'
        except Exception as e:
            logging.error(f"Error classifying job by keywords: {e}")
            return 'Error'

    @staticmethod
    def extract_job_data(html_content, divs):
        outer_div = BeautifulSoup(html_content, 'html.parser')
        
        # Initialize dictionaries to hold extracted data
        job_data = {
            'job_titles': [],
            'job_location': [],
            'job_company': [],
            'job_url': [],
            'job_type': [],
        }

        try:
            # Extract job titles 
            job_title_element = outer_div.find(divs[0][0], class_=divs[0][1])
            if job_title_element:
                job_data['job_titles'].append(job_title_element.get_text(strip=True))
            else:
                job_data['job_titles'].append(np.nan)
            logging.info(f"Extracted Job Title: {job_data['job_titles'][-1]}")

            # Extract job Location 
            location_element = outer_div.find(divs[1][0], class_=divs[1][1])
            if location_element:
                job_data['job_location'].append(location_element.get_text(strip=True))
            else:
                job_data['job_location'].append(np.nan)
            logging.info(f"Extracted Job Location: {job_data['job_location'][-1]}")

            # Extract job URL 
            if divs[2][0] != '0':
                url_element = outer_div.find(divs[2][0], class_=divs[2][1])
                if url_element and url_element.get('href'):
                    job_data['job_url'].append(url_element.get('href'))
                else:
                    job_data['job_url'].append(np.nan)
            else:
                job_data['job_url'].append(divs[2][1])
            logging.info(f"Extracted Job URL: {job_data['job_url'][-1]}")

            # Extract job company
            company_element = divs[3]
            if isinstance(company_element, str):
                job_data['job_company'].append(company_element)
            elif company_element:
                job_data['job_company'].append(company_element.get_text(strip=True))
            else:
                job_data['job_company'].append(np.nan)
            logging.info(f"Extracted Job Company: {job_data['job_company'][-1]}")

            # Extract job type
            type_element = WebScraper.classify_job_by_keywords(job_data['job_titles'][-1])
            job_data['job_type'].append(type_element)
            logging.info(f"Classified Job Type: {type_element}")

        except Exception as e:
            logging.error(f"Error extracting job data: {e}")

        return job_data

    @staticmethod
    def process_html_data(html_data_list, divs):
        all_job_data = {
            'job_company': [],
            'job_titles': [],
            'job_location': [],
            'job_url': [],
            'job_type': [],
        }

        try:
            for i, html_content in enumerate(html_data_list):
                logging.info(f"Processing HTML data from page {i+1}")
                job_data = WebScraper.extract_job_data(html_content, divs)

                all_job_data['job_titles'].extend(job_data['job_titles'])
                all_job_data['job_location'].extend(job_data['job_location'])
                all_job_data['job_company'].extend(job_data['job_company'])
                all_job_data['job_url'].extend(job_data['job_url'])
                all_job_data['job_type'].extend(job_data['job_type'])

            df = pd.DataFrame(all_job_data)
            df.to_csv('Data.csv')
            logging.info("Data successfully saved to 'Data.csv'.")

        except Exception as e:
            logging.error(f"Error processing HTML data: {e}")

    @staticmethod
    def scrape_job_data_static(url, out_div, divs):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        html_data_list = []
        try:
            driver.get(url)
            logging.info(f"Started scraping data from {url}")

            for i in range(1):
                logging.info(f"Scraping Page {i + 1}")
                time.sleep(2)
                try:
                    outer_div = driver.find_element(By.CLASS_NAME, out_div[0])
                    html_content = outer_div.get_attribute('outerHTML')
                    html_data_list.extend(html_content)
                    logging.info(f"HTML Content from Page {i + 1}: {html_content}")

                    # Handle possible click interception errors
                    try:
                        link = driver.find_element(By.CLASS_NAME, out_div[1])
                        if link:
                            # Scroll the element into view before clicking
                            driver.execute_script("arguments[0].scrollIntoView(true);", link)
                            action = ActionChains(driver)
                            action.move_to_element(link).click().perform()
                            logging.info(f"Navigated to Page {i + 1}")
                        else:
                            logging.warning(f"Next page link not found at page {i + 1}")
                            break
                    except ElementClickInterceptedException:
                        logging.error(f"Element click intercepted at page {i + 1}. Retrying...")
                        time.sleep(5)  # wait before retrying
                        continue  # Retry the click operation
                    except Exception as e:
                        logging.error(f"Error on page {i + 1}: {e}")
                        break

                except Exception as e:
                    logging.error(f"Error on page {i + 1}: {e}")
                    break

        except Exception as e:
            logging.error(f"Error scraping job data from {url}: {e}")

        driver.quit()  # Close the browser after scraping
        logging.info("Browser session ended.")
        WebScraper.process_html_data(html_data_list, divs)
