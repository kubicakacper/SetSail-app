from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

# FREE-WAVE, EUROMARINE, SAILING EUROPE


def pricelistFreeWave():

    pricelist_FreeWave = "https://www.free-wave.at/preisliste/"
    url = requests.get(pricelist_FreeWave)
    soup = BeautifulSoup(url.content, 'html.parser')


    pd.set_option("display.max_rows", None, "display.max_columns", None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    dF_list = pd.read_html(str(soup.find('table')))[0]
    dF = pd.DataFrame(dF_list)
    dF = dF.drop(index=0).drop(index=len(dF.index)-1)
    return dF


def yachtsFreeWave():

    yachts_FreeWave = "https://www.free-wave.at/yachten/"
    url = requests.get(yachts_FreeWave)
    soup = BeautifulSoup(url.content, 'html.parser')
    yachtSection = soup.find('section', {"class": "latest-yachts"})
    yachtList = yachtSection.find_all('div', {'class': 'list-boat-content'})
    for yacht in yachtList:
        # yacht = yachtList[0]
        yachtTag = yacht.select("a")[0]
        yachtUrl = yachtTag['href']
        print('\nLink do jachtu: ' + yachtUrl)
        yachtPage = requests.get(yachtUrl)
        yachtSoup = BeautifulSoup(yachtPage.content, 'html.parser')

        print('\nNazwa jachtu: ' + yachtSoup.find('h1').text.split(sep='\n')[1].strip())

        technicalData_dF = pd.DataFrame(columns=["key", "value"])
        technicalDataItems = yachtSoup.find('div', {'class': 'entry tech-block'}).find('ul').find_all('li')
        for item in technicalDataItems:
            if (item.span.contents == []):
                item.span.contents = ['Unknown']
            dict = {'key': item.contents[0], 'value': item.span.contents[0]}
            tempDF = pd.DataFrame([dict])
            # technicalData_dF = technicalData_dF.append(dict, ignore_index=True)
            technicalData_dF = pd.concat([technicalData_dF, tempDF], ignore_index=True, axis=0)

        print('\nSzczegoly techniczne jachtu:')
        print(technicalData_dF)

        priceList_DF = pd.DataFrame(columns=['period', 'price'])
        priceList = yachtSoup.find('table', {'class': 'single-prices'}).find_all('tr')
        deposit = priceList[len(priceList) - 1].find_all('td')[1].get_text()
        for item in priceList:
            dict = {'period': item.find_all('td')[0].contents[0].replace(" ", ""),
                    'price': item.find_all('td')[1].contents[0]}
            tempDF = pd.DataFrame([dict])
            priceList_DF = pd.concat([priceList_DF, tempDF], ignore_index=True, axis=0)
        priceList_DF = priceList_DF[:-1]
        print('\nCennik jachtu w tym roku jest nastepujacy:')
        print(priceList_DF)
        print('\nKaucja za jacht wynosi: ' + deposit)
