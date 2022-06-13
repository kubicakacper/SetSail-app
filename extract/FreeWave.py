from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# Free-Wave has a pricelist site, where there is a pretty 2D (yachts x period) table to ingest
# and a yachts site, where You need to do some webcrawling

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def pricelistFreeWave():

    pricelistFreeWave = "https://www.free-wave.at/preisliste/"
    url = requests.get(pricelistFreeWave)
    soup = BeautifulSoup(url.content, 'html.parser')

    dF_list = pd.read_html(str(soup.find('table')))[0]
    dF = pd.DataFrame(dF_list)
    dF = dF.drop(index=0).drop(index=len(dF.index)-1)
    return dF


def yachtsFreeWave():

    yachtsFreeWave = "https://www.free-wave.at/yachten/"
    url = requests.get(yachtsFreeWave)
    soup = BeautifulSoup(url.content, 'html.parser')
    yachtSection = soup.find('section', {"class": "latest-yachts"})
    yachtList = yachtSection.find_all('div', {'class': 'list-boat-content'})
    for yacht in yachtList:
        yachtTag = yacht.select("a")[0]
        yachtUrl = yachtTag['href']
        print('\nLink to the yacht: ' + yachtUrl)
        yachtPage = requests.get(yachtUrl)
        yachtSoup = BeautifulSoup(yachtPage.content, 'html.parser')

        # print('\nYacht\'s name: ' + yachtSoup.find('h1').text.split(sep='\n')[1].strip())

        technicalDataDF = pd.DataFrame(columns=["key", "value"])

        # Beacause the frame.append method is deprecated and will be removed from pandas in a future version,
        # I am using pandas.concat instead.
        dict = {'key': 'NAME', 'value': yachtSoup.find('h1').text.split(sep='\n')[1].strip()}
        technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)

        technicalDataItems = yachtSoup.find('div', {'class': 'entry tech-block'}).find('ul').find_all('li')
        for item in technicalDataItems:
            if (item.span.contents == []):
                item.span.contents = ['Unknown']
            dict = {'key': item.contents[0].strip(), 'value': item.span.contents[0].strip()}
            technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)
        dict = {'key': 'Location', 'value': 'Trogir (Seget Marina Baotic)'}
        technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)

        print('\nYacht\'s specs:')
        print(technicalDataDF)

        # BELOW IS SCRAPING OF THE PRICELIST TABLE FROM THE PARTICULAR YACHT'S PAGE

        # priceListDF = pd.DataFrame(columns=['period', 'price'])
        # priceList = yachtSoup.find('table', {'class': 'single-prices'}).find_all('tr')
        # # deposit = priceList[len(priceList) - 1].find_all('td')[1].get_text()
        # for item in priceList:
        #     dict = {'period': item.find_all('td')[0].contents[0].replace(" ", ""),
        #             'price': item.find_all('td')[1].contents[0]}
        #     tempDF = pd.DataFrame([dict])
        #     priceListDF = pd.concat([priceListDF, tempDF], ignore_index=True, axis=0)
        # priceListDF = priceListDF[:-1]
        # print('\nPricelist of the yacht this year is the following:')
        # print(priceListDF)

        # print('\nDeposit for the yacht: ' + deposit)


yachtsFreeWave()