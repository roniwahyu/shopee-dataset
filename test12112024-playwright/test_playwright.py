# !pip install playwright
# !playwright install
# !pip install nest_asyncio

import nest_asyncio
import asyncio
import pandas as pd
from playwright.sync_api import sync_playwright

nest_asyncio.apply()  # Apply to avoid conflicts in Jupyter

def scrape_shopee_products(start_url, max_pages=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(start_url)

        products = []

        for page_num in range(max_pages):
            print(f"Scraping page {page_num + 1}")
            
            # Wait for the product list to load
            page.wait_for_selector(".shopee-search-item-result__item")
            
            # Select all product containers
            product_wrappers = page.query_selector_all(".shopee-search-item-result__item")

            # Extract product information
            for wrapper in product_wrappers:
                name = wrapper.query_selector(".shopee-item-card__text-title").inner_text() if wrapper.query_selector(".shopee-item-card__text-title") else None
                price = wrapper.query_selector(".shopee-item-card__current-price").inner_text() if wrapper.query_selector(".shopee-item-card__current-price") else None
                link = wrapper.query_selector("a.shopee-item-card__link").get_attribute("href") if wrapper.query_selector("a.shopee-item-card__link") else None

                # Rating and sales info
                rating_sales = wrapper.query_selector(".mb-2.flex.items-center.space-x-1")
                rating = rating_sales.query_selector(".text-shopee-black87").inner_text() if rating_sales and rating_sales.query_selector(".text-shopee-black87") else None
                sales = rating_sales.query_selector(".text-shopee-black87.min-h-4").inner_text() if rating_sales and rating_sales.query_selector(".text-shopee-black87.min-h-4") else None

                products.append({
                    "Name": name,
                    "Price": price,
                    "Link": link,
                    "Rating": rating,
                    "Sales": sales
                })

            # Pagination: Click 'Next' button if available
            next_button = page.query_selector(".shopee-icon-button--right")
            if next_button:
                next_button.click()
                page.wait_for_timeout(2000)  # Wait for the next page to load
            else:
                break  # Exit if no more pages

        browser.close()

    # Convert to DataFrame
    return pd.DataFrame(products)

# Run the function in Jupyter
start_url = "https://shopee.co.id/search?keyword=laptop%20asus"
data_df = scrape_shopee_products(start_url, max_pages=5)
data_df.to_csv('shopee_products.csv', index=False)
data_df.head()
