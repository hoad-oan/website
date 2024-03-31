import yfinance as yf
import requests
from datetime import date, timedelta
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

# .download only shows the Open        High         Low       Close   Adj Close    Volume - it gives adj close price
# .info gives more information
class StockInfo:
    # class attribute, shared by all stock
    def __init__(self, ticker, adjClose, percentChange):
        # object attribute, specific to each stock object
        self.ticker = ticker
        self.adjClose = adjClose
        self.percentChange = percentChange

class main:
    listOfSP10 = ['MSFT', 'AAPL', 'NVDA', 'AMZN', 'META', 'GOOGL', 'BRK-B', 'GOOG', 'LLY', 'AVGO']
    listOfConstituents = []

    def getPriceAndPercentChange(ticker, previousOpenDate):
        todayStock = yf.download(ticker, start=previousOpenDate)
        adjClosePrices = todayStock["Adj Close"]
        # print(adjClosePrices)
        latestAdjClose = adjClosePrices.iloc[-1]
        previousAdjClose = adjClosePrices.iloc[-2]

        dailyChanges = (latestAdjClose - previousAdjClose)/previousAdjClose * 100
        return latestAdjClose, dailyChanges

    # find current open market date
    currentOpenDate = date.today()
    while currentOpenDate.weekday() in (5,6):
        currentOpenDate = currentOpenDate - timedelta(days=1)

    # find the previous open market date
    previousOpenDate = currentOpenDate - timedelta(days=1)
    while previousOpenDate.weekday() in (0,5,6): # if today is Monday and the previous date is when market close
        previousOpenDate = previousOpenDate - timedelta(days=1)

    # print(previousOpenDate)

    # for ticker in listOfSP10[0:1]:
    #     latestAdjClose, latestPercentChanges = getPriceAndPercentChange(ticker, previousOpenDate)
    #     constituent = StockInfo(ticker, latestAdjClose, latestPercentChanges)
    #     listOfConstituents.append(constituent)
    #     print("percent change: ", constituent.percentChange)
    #     print("last price: ", constituent.percentChange)
    
        def getCompanyInfo(tickerString):
            currStock = yf.Ticker(tickerString)
            # get all company info
            companyAllInfo = currStock.info
            # get sector and industry for classification
            companySector = companyAllInfo['sector']
            companyIndustry = companyAllInfo['industry']
            return companySector, companyIndustry

        
        def calculateDividendYield(tickerString, currentPosition):
            currStock = yf.Ticker(tickerString)
            # get all company info
            companyAllInfo = currStock.info
            # get dividend yield percentage
            dividendYieldPercent = companyAllInfo['dividendYield']
            dividendEarned = currentPosition * dividendYieldPercent
            # showcase last divident date
            lastDividendDate = companyAllInfo['lastDividendDate']
            return dividendEarned, lastDividendDate






