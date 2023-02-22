from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

def parse_item(html_page):
    results = []
    html = HTMLParser(html_page)
    data = html.css("a.grid-product__meta")
    for item in data:
        product = {
            "Katana Name": item.css_first("a.grid-product__meta").text().replace('\n',' '),
            "Price":item.css_first("div.grid-product__price").text().replace('\n',' ')
        }
        results.append(product)
    return results

def main():
    url = "https://katanakult.com/collections/katana"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless = False)
        page = browser.new_page()
        page.goto(url,wait_until = "networkidle")
        next_page = page.locator(".next")
        while True:
            print(parse_item(page.content()))
            if next_page.is_disabled():
                break
            page.click(".next")
            page.wait_for_load_state("networkidle")
            
if __name__ == "__main__":
    main()
        