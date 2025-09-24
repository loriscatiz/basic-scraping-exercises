from playwright.sync_api import sync_playwright
import json


def extract_quotes(page, base_url, current_page, data):
    if data is None:
        data = []

    print(f"\n===== CURRENT PAGE: {current_page} =====\n")
    page.goto(f"{base_url}/page/{current_page}")
    page.wait_for_selector(".quote")
    quotes = page.query_selector_all(".quote")
    for quote in quotes:
        author = quote.query_selector(".author").text_content()
        text = quote.query_selector(".text").text_content()
        data.append(
            {
                "author": author,
                "text": text,
            }
        )
    return data


def main():
    data = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        STARTING_PAGE = 1
        ENDING_PAGE = 7
        BASE_URL = "https://quotes.toscrape.com/js"
        current_page = STARTING_PAGE
        while current_page <= ENDING_PAGE:
            data = extract_quotes(
                page=page, base_url=BASE_URL, current_page=current_page, data=data
            )
            current_page += 1

        browser.close()
    with open("quotes_spa.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
