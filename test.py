from dotenv import load_dotenv
from selenium import webdriver
import time
import os
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        user_name = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        user_name.send_keys(os.getenv("I_USERNAME"))
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(os.getenv("I_PASSWORD"))
        time.sleep(3)

        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        time.sleep(7)

        try:
            save_login_prompt = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not now')]")))
            save_login_prompt.click()
            print("Clicked 'Not now' on save login prompt.")
        except TimeoutException:
            print("No save login prompt found.")

        try:
            notifications_prompt = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]")))
            notifications_prompt.click()
            print("Clicked 'Not Now' on notifications prompt.")
        except TimeoutException:
            print("No notifications prompt found.")

    def find_followers(self):
        self.driver.get("https://www.instagram.com/germany.explores/followers/")
        time.sleep(5)

        try:
            followers_link = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a/span')
            ))
            followers_link.click()
            print("Opened followers modal.")
        except TimeoutException:
            print("Could not open followers modal.")
            return

        modal_xpath = "//div[contains(@class, 'x1i10hfl')]//div[contains(@class, 'x9f619') and contains(@class, 'x1n2onr6')]"
        try:
            modal = self.wait.until(EC.presence_of_element_located((By.XPATH, modal_xpath)))
            for _ in range(5):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)
            print("Scrolled followers modal.")
        except TimeoutException:
            print("Followers modal not found with updated XPath.")

    def follow(self):
        time.sleep(5)
        follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._acan._acap._acas._aj1-._ap30")
        print(f"Found {len(follow_buttons)} 'Follow' buttons.")

        max_follows = 20  # Limit to 20 follows to avoid rate limits
        follow_count = 0

        for i, button in enumerate(follow_buttons, 1):
            if follow_count >= max_follows:
                print(f"Reached follow limit of {max_follows}. Stopping.")
                break

            try:
                # Scroll button into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.5)
                self.wait.until(EC.element_to_be_clickable(button))
                button.click()
                print(f"Clicked Follow button {i}")
                follow_count += 1
                time.sleep(3)  # Increased delay to 3 seconds to avoid rate limits
            except ElementClickInterceptedException:
                print(f"Follow button {i} intercepted, attempting to resolve...")
                try:
                    # Check for "Try Again Later" dialog
                    ok_button = self.wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(), 'OK')]")
                    ))
                    ok_button.click()
                    print("Clicked 'OK' on 'Try Again Later' dialog. Pausing for 5 minutes...")
                    time.sleep(300)  # Pause for 5 minutes before retrying
                    # Retry clicking the same button
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    self.wait.until(EC.element_to_be_clickable(button))
                    button.click()
                    print(f"Retried and clicked Follow button {i}")
                    follow_count += 1
                    time.sleep(3)
                except TimeoutException:
                    print("No 'OK' button found, trying JavaScript click...")
                    try:
                        self.driver.execute_script("arguments[0].click();", button)
                        print(f"Clicked Follow button {i} with JavaScript.")
                        follow_count += 1
                        time.sleep(3)
                    except:
                        print(f"JavaScript click failed for button {i}, skipping.")
            except TimeoutException:
                print(f"Follow button {i} not clickable, skipping.")
            except Exception as e:
                print(f"Unexpected error on button {i}: {e}, skipping.")

bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()