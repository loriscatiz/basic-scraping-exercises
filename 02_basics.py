import requests
from bs4 import BeautifulSoup

import json


def write_to_json(file_name: str, data: list, indent=2) -> None:
    with open(file_name, "w") as f:
        json.dump(data, f, indent=indent)


def main():
    url = "https://quotes.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    data = []

    if response.status_code == 200:
        quotes = soup.select(".quote")
        for quote in quotes:
            text = quote.select(".text")[0].text
            author = quote.select(".author")[0].text
            if text and author:
                data.append({"Author": author, "Text": text})
            else:
                data.append("Something went wrong with this quote")

        write_to_json("data.json", data)

    else:
        print(f"Failed to retrieve page: {response.status_code}")


if __name__ == "__main__":
    main()
