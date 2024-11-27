import asyncio
import pandas as pd
from playwright.async_api import async_playwright

# Define the main async scraping function
async def scrape_shopee_products(start_url, max_pages=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(start_url)
        
        products = []

        for page_num in range(max_pages):
            print(f"Scraping page {page_num + 1}")
            
            # Wait for the product list to load
            await page.wait_for_selector(".shopee-search-item-result__item")
            
            # Select all product containers
            product_wrappers = await page.query_selector_all(".shopee-search-item-result__item")

            # Extract product information
            for wrapper in product_wrappers:
                name = await wrapper.query_selector(".shopee-item-card__text-title")
                price = await wrapper.query_selector(".shopee-item-card__current-price")
                link = await wrapper.query_selector("a.shopee-item-card__link")
                
                # Rating and sales info
                rating_sales = await wrapper.query_selector(".mb-2.flex.items-center.space-x-1")
                rating = await rating_sales.query_selector(".text-shopee-black87") if rating_sales else None
                sales = await rating_sales.query_selector(".text-shopee-black87.min-h-4") if rating_sales else None

                products.append({
                    "Name": await name.inner_text() if name else None,
                    "Price": await price.inner_text() if price else None,
                    "Link": await link.get_attribute("href") if link else None,
                    "Rating": await rating.inner_text() if rating else None,
                    "Sales": await sales.inner_text() if sales else None
                })

            # Pagination: Click 'Next' button if available
            next_button = await page.query_selector(".shopee-icon-button--right")
            if next_button:
                await next_button.click()
                await page.wait_for_timeout(2000)  # Wait for the next page to load
            else:
                break  # Exit if no more pages

        await browser.close()

    # Convert to DataFrame
    return pd.DataFrame(products)

# Run the async function using asyncio.run()
if __name__ == "__main__":
    start_url = "https://shopee.co.id/search?keyword=asus%20laptop"
    data_df = asyncio.run(scrape_shopee_products(start_url, max_pages=5))
    data_df.to_csv('shopee_products.csv', index=False)
    print(data_df.head())
