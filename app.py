# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
from scrab import WebScraper

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def scrape():
    if request.method == "POST":
        # Get form data
        url = request.form.get('url')
        outer_div_class = request.form.get('outer_div')
        load_more_css = request.form.get('load_more_css')
        next_page_css = request.form.get('next_page_css')

        # Fetch dynamic column data from the form
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

        # For simplicity, assuming the page type is dynamic (modify as needed)
        scraped_data = scraper.dynamic_webpage(url, load_more_css, next_page_css, outer_div_class, columns)

        # Close the scraper
        scraper.close()

        # Write the scraped data to a CSV file
        with open("scraped_data.csv", mode="w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=[col['name'] for col in columns])
            writer.writeheader()
            writer.writerows(scraped_data)

        # Redirect to a success page
        return redirect(url_for("success"))

    return render_template("index.html")


@app.route("/success")
def success():
    return "Data successfully scraped and saved to scraped_data.csv!"


if __name__ == "__main__":
    app.run(debug=True)
