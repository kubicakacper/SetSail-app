from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# Kufner has a price-list site, where there is a pretty 2D (yachts x period) table to ingest
# and a yachts site, where You need to do some web-crawling

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def pricelist():

    print(f'I am in ek.pricelist\n')

    pricelist_kufner = "https://nautika-kufner.hr/price-list/"
    url = requests.get(pricelist_kufner)
    soup = BeautifulSoup(url.content, 'html.parser')
    df_list = pd.read_html(str(soup.find('table')).replace("<br/>", " AND "))[0]
    return pd.DataFrame(df_list)


def yachts():

    print(f'I am in ek.yachts\n')

    yachts_kufner = "https://nautika-kufner.hr/fleet/"
    url = requests.get(yachts_kufner)
    soup = BeautifulSoup(url.content, 'html.parser')
    yacht_list = soup.find_all('div', {'class': re.compile(
        r'col-mD-4 col-sm-4 col-xs-12 col-xxs-12 stm-isotope-listing-item all')})

    list_of_dfs = []

    for yacht in yacht_list:
        yacht_tag = yacht.select("a")[0]
        yacht_url = yacht_tag['href']
        yacht_page = requests.get(yacht_url)
        yacht_soup = BeautifulSoup(yacht_page.content, 'html.parser')

        yacht_div = yacht_soup.find('div', {'class': 'boat row'})

        technical_data_df = pd.DataFrame(columns=["key", "value"])

        # Because the frame.append method is deprecated and will be removed from pandas in a future version,
        # I am using pandas.concat instead.
        yacht_as_dict = {'key': 'NAME', 'value': yacht_div.h2.text.strip()}
        technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])], ignore_index=True, axis=0)

        technical_data_items = yacht_soup.find('div', {'class': 'boat-data row'}).find_all('div', {'class': 't-row'})
        for item in technical_data_items[0:-1]:
            key_div = item.find_next('div', {'class': 't-label'})
            if key_div is not None:
                key_item = key_div.text.strip()
                value_item = item.find_next('div', {'class': 't-value h6'}).text.strip()
                yacht_as_dict = {'key': key_item, 'value': value_item}
                technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])], ignore_index=True,
                                              axis=0)

        technical_data_items_2 = yacht_soup.find_all('div', {'class': 'top-table'})
        for table in technical_data_items_2:
            rows = table.find_all('tr')
            for item in rows:
                key_div = item.find('span', {'class': 'text-left'})
                if key_div is not None:
                    key_item = key_div.text.strip()
                    value_item = item.find('span', {'class': 'text-right'}).text.strip()
                    yacht_as_dict = {'key': key_item, 'value': value_item}
                    technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])],
                                                  ignore_index=True, axis=0)

        yacht_as_dict = {'key': 'yacht URL', 'value': yacht_url}
        technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])], ignore_index=True, axis=0)
        technical_data_df = technical_data_df.T
        technical_data_df.columns = technical_data_df.iloc[0]
        technical_data_df = technical_data_df[1:]
        list_of_dfs.append(technical_data_df)

    all_yachts_df = pd.DataFrame(list_of_dfs[0])
    for df in list_of_dfs[1:]:
        all_yachts_df = pd.concat([all_yachts_df, df])

    all_yachts_df = all_yachts_df.reset_index(drop=True)

    return all_yachts_df
