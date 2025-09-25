from playwright.sync_api import Browser, Page, Page, sync_playwright
import json


def get_categories_links(page: Page):
    print("=== GETTING LINKS ===")
    links: dict[str, str] = {}
    nav_links_el = page.query_selector_all(".nav-list a")
    for el in nav_links_el:
        href = el.get_attribute("href")
        category = el.inner_text()
        if category and href and category.lower() != "books":
            print(category, href)
            links.update({category: href})
    return links


def extract_books(page: Page):
    data: list[dict[str, str | float | int]] = []
    title = ""
    price = ""
    rating = ""

    print("=== SCRAPING BOOKS ===")
    products = page.query_selector_all(".product_pod")
    for product in products:
        img_el = product.query_selector(".thumbnail")
        if img_el is not None:
            title = img_el.get_attribute("alt")

        rating_el = product.query_selector(".star-rating")
        if rating_el is not None:
            rating_classes = rating_el.get_attribute("class")
            if rating_classes is not None and len(rating_classes) > 1:
                rating = rating_classes.split(" ")[1]
                match rating.lower():
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

        price_el = product.query_selector(".price_color")
        if price_el is not None:
            price_text = price_el.text_content()
            if price_text is not None:
                price = price_text.replace("£", "")
                price = float(price)

        if title and rating and price:
            data.append(
                {
                    "title": title,
                    "rating": rating,
                    "price": price,
                }
            )
        else:
            data.append({"error": "something wrong happened"})

    return data


def main():
    data = {}
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=True)
        page: Page = browser.new_page()
        BASE_URL = "https://books.toscrape.com"
        page.goto(BASE_URL)
        links = get_categories_links(page)
        for cat, link in links.items():
            print("=== SCRAPING PER CATEGORY ===")
            print(f"category: {cat}")
            category_data = []
            category_url = f"{BASE_URL}/{link}"

            page.goto(category_url)
            while True:
                category_data.extend(extract_books(page))
                next_el = page.query_selector(".pager .next a")
                if next_el is not None:
                    next_el.click()
                else:
                    break

            data.update({cat: category_data})

    with open("books_playwright.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
