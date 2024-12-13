import pandas as pd
from scrab import WebScraper
from bs4 import BeautifulSoup
import os

# Load the Excel file
df = pd.read_excel('final_input.xlsx')
for ind, row in df.iterrows():
    print(f"Processing: {row['Name']}")


    url = row['CareersLink']
    out_div = [row['Outer_div'], row['next']]
    
    # Define divs structure based on Excel data
    divs = [
        [row['Title_tag'], row['Title_attr_key'], row['Title_attr_value']],
        [row['Link_tag'], row['Link_attr_key'], row['Link_attr_value']],
        [row['Location_tag'], row['Location_attr_key'], row['Location_attr_value']],
        row['Name']
    ]
    
    WebScraper.scrape_job_data_static(url, out_div, divs)
