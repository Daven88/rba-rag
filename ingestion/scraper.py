import requests
from bs4 import BeautifulSoup
import datetime

BASE_URL = 'https://www.rba.gov.au'
YEARS = list(range(2006, datetime.date.today().year + 1))

def get_year_links(years) -> list[str]:
    date_link_list = []
    for year in years:
        date_link_list.append(f'https://www.rba.gov.au/monetary-policy/rba-board-minutes/{year}/')
    return date_link_list

def get_minutes_links(years) -> list[str]:
    date_link_list = get_year_links(years)
    minutes_urls = []
    for date in date_link_list:
        response = requests.get(date)
        soup = BeautifulSoup(response.text, 'lxml')
        for tag in soup.select("li a"):
            href = tag['href']
            if href.endswith('.html') and '/rba-board-minutes/' in href:
                minutes_urls.append(BASE_URL + href)
    return minutes_urls
    
def get_minutes_text(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.find(id="content").get_text(separator="\n", strip=True)


if __name__ == "__main__":
    links = get_minutes_links(YEARS)
    print(get_minutes_text(links[0])[:500])
    print(f"Found {len(links)} links")
    for link in links[:5]:
        print(link)