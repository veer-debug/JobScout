import pandas as pd
from scrab import WebScraper
import os

df=pd.read_excel('Data_scrabing\companies.xlsx')
for ind,row in df.iterrows():
    url=row['CareersLink']
    out_div=[row['Outer_div'],row['If Dynamic_xpa']]
    divs=[[row['Name_div_tag'],row['Name_div']],[row['Location_div_tag'],row['Location_div']],[row['Url_div_tag'],row['Url_div']],row['Name']]
    WebScraper.scrape_job_data_static(url,out_div,divs)
    