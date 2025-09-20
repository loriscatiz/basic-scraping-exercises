import requests
from bs4 import BeautifulSoup


def main():
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    if data.status_code == 200:
        title_el = soup.find("h1")
        title = title_el.text
        links = soup.select("a[href]")

        print(f"Title: {title}")
        print(f"Link count: {len(links)}")

    else:
        print(f"Failed to retrieve page: {data.status_code}")


if __name__ == "__main__":
    main()
