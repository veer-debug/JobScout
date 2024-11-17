import pandas as pd
from scrab import WebScraper
import os

df=pd.read_excel('Carears_pages.xlsx')
df.rename(columns={'If Dynamic_xpath': 'next'}, inplace=True)
for ind,row in df.iterrows():
    if ind==1:
        print(row['Name'])
        url=row['CareersLink']
        print(type(row['next']))
        out_div=[row['Outer_div'],row['next']]
        divs=[[row['Name_div_tag'],row['Name_div']],[row['Location_div_tag'],row['Location_div']],[row['Url_div_tag'],row['Url_div']],row['Name']]
        print(divs)
        WebScraper.scrape_job_data_static(url,out_div,divs)

    # print(url)
    # print(out_div)

    