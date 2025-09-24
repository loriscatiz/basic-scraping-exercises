from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/js/")
    page.wait_for_selector(".quote")
    quotes = page.query_selector_all(".quote")
    for quote in quotes:
        author = quote.query_selector(".author")
        text = quote.query_selector(".text")
        print(f"\n\n=====QUOTE=====\n\n")
        if text is not None and author is not None:
            print(f"{text.text_content()}\nby: {author.text_content()}")
        else:
            print(f"something's wrong, I can feel it")

    browser.close()
