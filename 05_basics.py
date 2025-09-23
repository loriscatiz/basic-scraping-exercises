import requests
import time
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get_response(
    url: str, headers: dict[str, str] = HEADERS
) -> requests.Response | None:
    time.sleep(1)
    response = requests.get(url, headers)
    response.encoding = "utf-8"
    if response.status_code == 200:
        print("RESPONSE STATUS OK")
        return response
    else:
        print("Error: ", response.status_code)


def has_next_page(soup: BeautifulSoup) -> bool:
    return len(soup.select(".pager .next")) > 0


def get_authors_links(
    soup: BeautifulSoup, data: dict[str, str] | None = None
) -> dict[str, str]:
    if data is None:
        data = {}

    quotes = soup.select(".quote")

    for quote in quotes:
        path = quote.select("span a")[0]["href"]
        author = quote.select(".author")[0].text
        if path and author:
            data.update({author: f"{BASE_URL}{path}"})
        else:
            print("something is wrong")

    return data


def scrape_author(soap: BeautifulSoup, data):
    author = soap.select(".author-title")[0].text
    location = soap.select(".author-born-location")[0].text
    date = soap.select(".author-born-date")[0].text
    data.update({author: {"location": location, "date": date}})
    return data


def main():
    response = get_response(BASE_URL)
    current_page = 1
    data = {}
    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        links = get_authors_links(soup)
        while has_next_page(soup):
            current_page += 1
            response = get_response(f"{BASE_URL}/page/{current_page}")
            if response:
                soup = BeautifulSoup(response.text, "html.parser")
                links = get_authors_links(soup, links)

        for _, link in links.items():
            response = get_response(link)
            if response:
                soup = BeautifulSoup(response.text, "html.parser")
                data = scrape_author(soup, data)

        with open("links.json", "w") as f:
            json.dump(links, f, indent=2)

        with open("authors_details.json", "w") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
