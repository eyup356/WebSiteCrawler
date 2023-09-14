import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

target_url = "http://oppenheimer.com"
found_links = set()
def make_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
    except requests.exceptions.RequestException:
        pass
    return None
def crawl(url):
    soup = make_request(url)
    if soup is None:
        return
    for link in soup.find_all('a'):
        found_link = link.get('href')
        if found_link:
            found_link = urljoin(url, found_link)
            parsed_url = urlparse(found_link)
            if parsed_url.netloc == urlparse(target_url).netloc:
                if "#" in parsed_url.fragment:
                    parsed_url = parsed_url._replace(fragment='')
                found_link = parsed_url.geturl()
                if found_link not in found_links:
                    found_links.add(found_link)
                    print(found_link)
                    crawl(found_link)
crawl(target_url)
