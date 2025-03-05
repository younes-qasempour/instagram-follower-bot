from dotenv import load_dotenv
from selenium import webdriver
import time
import os

from selenium.webdriver.common.by import By

load_dotenv()


class InstaFollower:

    def __init__(self):
        # Optional - Keep browser open (helps diagnose issues during a crash)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        user_name = self.driver.find_element(By.NAME, "username")
        user_name.send_keys(os.getenv("I_USERNAME"))
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(os.getenv("I_PASSWORD"))
        time.sleep(3)

        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        time.sleep(7)

        # Click "Not now" and ignore Save-login info prompt
        save_login_prompt = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        if save_login_prompt:
            save_login_prompt.click()
        time.sleep(5)

        # # Click "not now" on notifications prompt
        # notifications_prompt = self.driver.find_element(by=By.XPATH, value="// button[contains(text(), 'Not Now')]")
        # if notifications_prompt:
        #     notifications_prompt.click()

    def find_followers(self):
        self.driver.get("https://www.instagram.com/germany.explores/followers/")
        time.sleep(5)

        self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]'
                                           '/section/main/div/header/section[3]/ul/li[2]/div/a/span').click()
        time.sleep(5)

        modal_xpath = ("/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/"
                       "div[2]/div")
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)
        for i in range(10):
            # In this case we're executing some Javascript, that's what the execute_script() method does.
            # The method can accept the script as well as an HTML element.
            # The modal in this case, becomes the arguments[0] in the script.
            # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)


    def follow(self):
        pass


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()