import pandas as pd
from scrab import WebScraper
import os

def load_companies_from_excel(file_path):
    """Load companies data from Excel and format it for scraping."""
    companies = []
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        # Split the columns into lists based on commas
        columns = []
        column_names = row['Column Names'].split(',')
        column_classes = row['Column Classes'].split(',')
        column_types = row['Column Types'].split(',')

        for name, class_, type_ in zip(column_names, column_classes, column_types):
            columns.append({
                'name': name.strip(),
                'class': class_.strip(),
                'type': type_.strip()
            })

        # Add company configuration to the list
        companies.append({
            'name': row['Company Name'],
            'url': row['URL'],
            'outer_div_class': row['Outer Div Class'],
            'columns': columns,
            'page_type': row['Page Type'].strip()
        })

    return companies

def save_data_to_csv(data, filename):
    """Save scraped data to a CSV file."""
    df = pd.DataFrame(data)
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)  # Append to existing file
    else:
        df.to_csv(filename, index=False)  # Create new file

def main():
    # Load the company details from the Excel file
    # companies = load_companies_from_excel("companies.xlsx")
    companies=['https://www.google.com/about/careers/applications/jobs/results/']

    # Initialize the WebScraper
    scraper = WebScraper()
    
    # List to store all scraped data
    all_scraped_data = []

    # Loop through each company and scrape the data
    for company in companies:
        print(f"Scraping data for {company['name']}...")

        # Choose the correct method based on the page type
        if company['page_type'] == "infinite_scroll":
            data = scraper.infinite_scroll(company['url'], company['outer_div_class'], company['columns'])
        elif company['page_type'] == "dynamic":
            data = scraper.dynamic_webpage(company['url'], None, None, company['outer_div_class'], company['columns'])
        else:
            data = scraper.static_page(company['url'], company['outer_div_class'], company['columns'])

        # Append the scraped data to the list
        for item in data:
            item['Company'] = company['name']  # Add company name to each item
            all_scraped_data.append(item)

        print(f"Data for {company['name']}: {data}")

    # Save all scraped data to CSV
    save_data_to_csv(all_scraped_data, 'scraped_data.csv')

    # Close the scraper
    scraper.close()

if __name__ == "__main__":
    main()
