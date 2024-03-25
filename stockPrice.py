import yfinance as yf
import requests
from bs4 import BeautifulSoup

# URL of the S&P 500 index page on the official S&P Dow Jones Indices website
url = 'https://www.spglobal.com/spdji/en/indices/equity/sp-500/#data'
getDataFromPage = False


if getDataFromPage:
    try:
        response = requests.get(url)
        # parse the HTML content of the page
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # find the table that we need the content from
            section = soup.find('section', class_='data-constituents table-divider detail-data-widgets')

            # Check if the section is found
            if section:
                # Find all divs within the section with the desired class(es)
                divs = section.find_all('div', class_='column-label mobile-only')

                # Loop through each div
                for div in divs:
                    # Extract the content within the span tags inside the div
                    spans = div.find_all('span')
                    for span in spans:
                        span_content = span.text.strip()  # Extract text content of each span
                        print(span_content)
            else:
                print("Section with the specified class name not found.")

        else:
            print("Failed to retrieve data from the website. Status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", e)

class Stock:
    # class attribute, shared by all stock
    def __init__(self, ticker):
        # object attribute, specific to each stock object
        self.ticker = ticker
        self.adjClose = ticker.info('Adj Close')
        self.precentChange = ticker.info('get_percent_change()')

class main:
    listOfSP10 = ['MSFT', 'APPL', 'NVDA', 'AMZN', 'META', 'GOOGL', 'BRK.B', 'GOOG', 'LLY', 'AVGO']
    listOfConstituents = []
    for ticker in listOfSP10:
        constituent = Stock(ticker)
        listOfConstituents.append(constituent)
