import requests
import time
from bs4 import BeautifulSoup
import json
import csv


def scrape_page(
    soup: BeautifulSoup,
    data: list[dict[str, str]] | None = None,
):
    if data is None:
        data = []

    prods = soup.select(".product_pod")

    for p in prods:
        entry = {}
        entry.update({"title": p.select(".thumbnail")[0]["alt"]})
        entry.update({"price": p.select(".price_color")[0].text.replace("£", "")})
        text_rating = p.select(".star-rating")[0]["class"][1].lower()
        match text_rating:
            case "one":
                rating = 1
            case "two":
                rating = 2
            case "three":
                rating = 3
            case "four":
                rating = 4
            case "five":
                rating = 5
            case _:
                rating = None
        entry.update({"rating": rating})
        data.append(entry)

    return data


def has_next_page(soup: BeautifulSoup):
    return len(soup.select(".pager .next")) > 0


def main():
    current_page = 1
    url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    time.sleep(1)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        data = scrape_page(soup)
        while has_next_page(soup) and current_page < 5:
            current_page += 1
            url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"
            response = requests.get(url, headers=headers)
            response.encoding = "utf-8"
            time.sleep(1)
            soup = BeautifulSoup(response.text, "html.parser")
            data = scrape_page(soup, data)
            print(url)

        with open("books.json", "w") as f:
            json.dump(data, f, indent=2)
        with open("books.csv", "w", newline="") as f:
            writer = csv.writer(
                f, delimiter="|", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(["TITLE", "PRICE", "RATING"])
            for entry in data:
                writer.writerow([entry["title"], entry["price"], entry["rating"]])


if __name__ == "__main__":
    main()
