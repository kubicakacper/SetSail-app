from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
import re

# Kufner has a pricelist site, where there is a pretty 2D (yachts x period) table to ingest
# and a yachts site, where You need to do some webcrawling

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def pricelist():

    print(f'I am in ek.pricelist\n')

    pricelistKufner = "https://nautika-kufner.hr/price-list/"
    url = requests.get(pricelistKufner)
    soup = BeautifulSoup(url.content, 'html.parser')
    # dF_list = pd.read_html(str(soup.find('table')).replace("<br/>","</th> <th scope=\"col\">"))[0]
    dF_list = pd.read_html(str(soup.find('table')).replace("<br/>"," AND "))[0]
    dF = pd.DataFrame(dF_list)
    return dF

def yachts():

    print(f'I am in ek.yachts\n')

    yachtsKufner = "https://nautika-kufner.hr/fleet/"
    url = requests.get(yachtsKufner)
    soup = BeautifulSoup(url.content, 'html.parser')
    yachtList = soup.find_all('div', {'class': re.compile(r'col-md-4 col-sm-4 col-xs-12 col-xxs-12 stm-isotope-listing-item all')})

    listOfDFs = []

    for yacht in yachtList:
        yachtTag = yacht.select("a")[0]
        yachtUrl = yachtTag['href']
        yachtPage = requests.get(yachtUrl)
        yachtSoup = BeautifulSoup(yachtPage.content, 'html.parser')

        yachtDiv = yachtSoup.find('div', {'class': 'boat row'})

        technicalDataDF = pd.DataFrame(columns=["key", "value"])

        # Beacause the frame.append method is deprecated and will be removed from pandas in a future version,
        # I am using pandas.concat instead.
        dict = {'key': 'NAME', 'value': yachtDiv.h2.text.strip()}
        technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)

        technicalDataItems = yachtSoup.find('div', {'class': 'boat-data row'}).find_all('div', {'class': 't-row'})
        for item in technicalDataItems[0:-1]:
            keyDiv = item.find_next('div', {'class': 't-label'})
            if(keyDiv != None):
                keyItem = keyDiv.text.strip()
                valueItem = item.find_next('div', {'class': 't-value h6'}).text.strip()
        #     if (item.span.contents == []):
        #         item.span.contents = ['Unknown']
            dict = {'key': keyItem, 'value': valueItem}
            technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)

        technicalDataItems_2 = yachtSoup.find_all('div', {'class': 'top-table'})
        for table in technicalDataItems_2:
            rows = table.find_all('tr')
            for item in rows:
                keyDiv = item.find('span', {'class': 'text-left'})
                if(keyDiv != None):
                    keyItem = keyDiv.text.strip()
                    valueItem = item.find('span', {'class': 'text-right'}).text.strip()
                    dict = {'key': keyItem, 'value': valueItem}
                    technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)

        dict = {'key': 'yacht URL', 'value': yachtUrl}
        technicalDataDF = pd.concat([technicalDataDF, pd.DataFrame([dict])], ignore_index=True, axis=0)
        # technicalDataDF = technicalDataDF.drop_duplicates().reset_index(drop=True)
        technicalDataDF = technicalDataDF.T
        technicalDataDF.columns = technicalDataDF.iloc[0]
        technicalDataDF = technicalDataDF[1:]
        listOfDFs.append(technicalDataDF)


    allYachtsDF = pd.DataFrame(listOfDFs[0])
    for df in listOfDFs[1:]:
        allYachtsDF = pd.concat([allYachtsDF, df])

    allYachtsDF = allYachtsDF.reset_index(drop=True)

    return allYachtsDF

        # BELOW IS SCRAPING OF THE PRICELIST TABLE FROM THE PARTICULAR YACHT'S PAGE

        # priceListDF = pd.DataFrame(columns=['period', 'price'])
        # priceListRows = yachtSoup.find('table', {'class': 'table pricelist'}).find_all('tr')
        #
        # keyItems = priceListRows[0].find_all('th')
        # keys = []
        # for item in keyItems[0:-1]:
        #     keys.append(item.text.strip())
        #
        # valueItems = priceListRows[1].find_all('td')
        # values = []
        # for item in valueItems[0:-1]:
        #     values.append(item.text.strip())
        #
        # for i in range(len(keys)):
        #     dict = {'period': keys[i], 'price': values[i]}
        #     priceListDF = pd.concat([priceListDF, pd.DataFrame([dict])], ignore_index=True, axis=0)
        # print('\nPricelist of the yacht this year is the following:')
        # print(priceListDF)
