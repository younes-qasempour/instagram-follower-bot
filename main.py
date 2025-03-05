from dotenv import load_dotenv
from selenium import webdriver
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
        user_name = self.driver.find_element(By.NAME, "username")
        user_name.send_keys(os.getenv("USERNAME"))

    def find_followers(self):
        pass

    def follow(self):
        pass


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()