import pytest
from playwright.sync_api import Page, expect
import csv
import asyncio
# Install necessary libraries if not already installed
# pip install pytest-playwright
# pip install pytest
# pip install playwright

# @pytest.mark.parametrize("keyword", ["baju","sandal"])
def test_shopee_search(page: Page, keyword: str):
    page.goto("https://shopee.co.id")

    # Accept cookies if the banner appears
    try:
        page.locator("button:has-text('Izinkan Semua Cookie')").click()
    except:
        pass  # Ignore if the cookie banner isn't found

    # Find the search input field and enter the keyword
    page.locator("input[placeholder='Cari di Shopee']").type(keyword)

    # Find the search button and click it
    page.locator("button[type='submit']").click()

    # Wait for the search results to load (adjust timeout if needed)
    page.wait_for_selector(".shopee-search-item-result__item")
    
    # Assert that the search results page is displayed
    expect(page).to_have_title(f"Cari {keyword} di Shopee Indonesia")
    
    # Check that at least one search result is displayed
    expect(page.locator(".shopee-search-item-result__item")).to_have_count(
      greater_than_or_equal_to=1
    )

    # Extract data (example: product titles) and save to CSV
    product_titles = []
    for item in page.locator(".shopee-search-item-result__item").all():
        try:
          product_titles.append(item.locator(".ie3A+4").inner_text())
        except:
          pass  # Handle cases where the selector might not be found

    # Write the results to a CSV file
    with open('search_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(["Product Title"])  # Header row
      writer.writerows([[title] for title in product_titles]) # Write each title as a separate row

# Run the async function using asyncio.run()
if __name__ == "__main__":
    start_url = "https://shopee.co.id/search?keyword=asus%20laptop"
    data_df = asyncio.run(test_shopee_search(start_url, "asus"))
    data_df.to_csv('shopee_products.csv', index=False)
    print(data_df.head())