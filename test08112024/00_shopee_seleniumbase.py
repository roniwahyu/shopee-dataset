import json
import random
import time
from seleniumbase import BaseCase
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class ShopeeScraper(BaseCase):
    def test_shopee_with_anti_bot_techniques(self):
        # Set up Chrome options for stealth mode
        chrome_options = self.get_chrome_options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--profile-directory=Default 1")
        chrome_options.add_argument("--incognito")
        
        # Rotate user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        
        # Set random viewport size
        width, height = random.randint(800, 1200), random.randint(600, 900)
        chrome_options.add_argument(f"--window-size={width},{height}")
        
        # Start browser with stealth options
        self.driver = self.get_new_driver(chrome_options=chrome_options)
        self.open("https://shopee.co.id")
        
        # Load cookies from JSON file
        with open("shopee.json", "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                # Remove unnecessary fields
                for field in ["sameSite", "storeId"]:
                    cookie.pop(field, None)
                self.driver.add_cookie(cookie)
        
        # Refresh page to activate cookies and session
        self.refresh()
        
        # Simulate some mouse movements
        action = ActionChains(self.driver)
        login_button = self.driver.find_element(By.CSS_SELECTOR, "a.navbar__link--account")
        action.move_to_element(login_button).perform()
        time.sleep(random.uniform(1.5, 3.5))  # Random delay to mimic human interaction
        
        # Check if we are logged in by searching for account-specific elements
        self.assert_text("Shopee", "title")
        
        # Interact with page elements with randomized delays
        self.open("https://shopee.co.id/search?keyword=speaker%20quran%20bluetooth")
        time.sleep(random.uniform(2, 5))  # Random delay before next action
        
        # Scroll randomly
        for _ in range(random.randint(2, 5)):
            self.scroll_to(random.randint(0, 500))
            time.sleep(random.uniform(1, 3))
