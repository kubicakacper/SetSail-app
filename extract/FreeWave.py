from bs4 import BeautifulSoup
import requests
import pandas as pd

# Free-Wave has a price-list site, where there is a pretty 2D (yachts x period) table to ingest
# and a yachts site, where You need to do some web-crawling

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def pricelist():

    print(f'I am in efw.pricelist\n')

    pricelist_free_wave = "https://www.free-wave.at/preisliste/"
    url = requests.get(pricelist_free_wave)
    soup = BeautifulSoup(url.content, 'html.parser')

    df_list = pd.read_html(str(soup.find('table')))[0]
    df = pd.DataFrame(df_list)
    df = df.drop(index=0).drop(index=len(df.index)-1)
    return df


def yachts():

    print(f'I am in efw.yachts\n')

    yachts_free_wave = "https://www.free-wave.at/yachten/"
    url = requests.get(yachts_free_wave)
    soup = BeautifulSoup(url.content, 'html.parser')
    yacht_section = soup.find('section', {"class": "latest-yachts"})
    yacht_list = yacht_section.find_all('div', {'class': 'list-boat-content'})

    list_of_dfs = []

    for yacht in yacht_list:
        yacht_tag = yacht.select("a")[0]
        yacht_url = yacht_tag['href']
        yacht_page = requests.get(yacht_url)
        yacht_soup = BeautifulSoup(yacht_page.content, 'html.parser')

        technical_data_df = pd.DataFrame(columns=["key", "value"])

        # Because the frame.append method is deprecated and will be removed from pandas in a future version,
        # I am using pandas.concat instead.
        yacht_as_dict = {'key': 'NAME', 'value': yacht_soup.find('h1').text.split(sep='\n')[1].strip()}
        technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])], ignore_index=True, axis=0)

        technical_data_items = yacht_soup.find('div', {'class': 'entry tech-block'}).find('ul').find_all('li')
        for item in technical_data_items:
            if not item.span.contents:
                item.span.contents = ['Unknown']
            yacht_as_dict = {'key': item.contents[0].strip(), 'value': item.span.contents[0].strip()}
            technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])], ignore_index=True, axis=0)
        yacht_as_dict = {'key': 'Location', 'value': 'Trogir (Seget Marina Baotic)'}
        technical_data_df = pd.concat([technical_data_df, pd.DataFrame([yacht_as_dict])], ignore_index=True, axis=0)

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
