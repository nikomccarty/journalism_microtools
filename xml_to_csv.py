# A script that converts xml to .csv that can be opened in Excel.
# This was created, specifically, to convert citations from DOIs, which are given in xml format.

from xml.etree import ElementTree
import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://doi.crossref.org/servlet/getForwardLinks?usr=hope@spectrumnews.org/spem&pwd=Marm0set15&doi=10.53053&startDate=2021-10-01&endDate=2022-03-23'
xml_data = requests.get(url).content

start_date = "2021-10-01"
end_date = "2022-04-14"

def parse_xml(xml_data):
    soup = BeautifulSoup(xml_data, 'xml')

    df = pd.DataFrame(columns=['citation_doi', 'journal_title', 'journal_abbrev', 'article_title', 'article_volume', 'article_year'])

    all_papers = soup.find_all('forward_link')
    print(f"Identified {len(all_papers)} citing papers.")   
    
    for index, item in enumerate(all_papers):
        volume = item.find('volume').text
        citation_doi = item.find('doi').text
        journal_title = item.find('journal_title').text
        article_title = item.find('article_title').text
        article_year = item.find('year').text

       # Adding extracted elements to rows in table
        row = {
            'citation_doi': citation_doi,
            'journal_title': journal_title,
            'article_title': article_title,
            'article_volume': volume,
            'article_year': article_year
        }

        df = df.append(row, ignore_index=True)
        df.to_csv('outputs/xml_conversion.csv')

    print("Conversion successful. Closing script...")
    print(df)

    return df

parse_xml(xml_data)