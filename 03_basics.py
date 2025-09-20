import requests
import time
from bs4 import BeautifulSoup

import json


def write_to_json(file_name: str, data: list, indent=2) -> None:
    with open(file_name, "w") as f:
        json.dump(data, f, indent=indent)


def scrape_page(response: requests.Response, data: list[dict[str, str]] = []):
    has_next_page = False
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.select(".quote")
        has_next_page = len(soup.select(".next")) > 0
        for quote in quotes:
            text = quote.select(".text")[0].text
            author = quote.select(".author")[0].text
            if text and author:
                data.append({"Author": author, "Text": text})
            else:
                data.append({"Error": "Something went wrong with this quote"})
    return (data, has_next_page)


def main(current_page=1, data=[]):
    base_url = "https://quotes.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    if current_page:
        url = base_url + f"page/{current_page}"
    else:
        url = base_url
    response = requests.get(url, headers=headers)

    print(
        f"""Executing...
current url: {url}
len data: {len(data)}
    """
    )

    (data, has_next_page) = scrape_page(response, data)
    if has_next_page:
        current_page += 1
        time.sleep(1)
        main(current_page, data)
    else:
        write_to_json("more_data.json", data)


if __name__ == "__main__":
    main()
