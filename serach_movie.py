# TODO: 继续重构 get_all_movies()
# TODO: 优化评级方式
# TODO: 影片无导演时 list index out of range

import bs4
import requests
import time
from urllib.parse import quote

from config.instantiate_driver import InstantiateDriver, user_agent
from bot import Bot
from locators.locators import Locators
from pages.pages import Pages


base_url = "https://search.douban.com/movie/subject_search?search_text={}&cat=1002"


class SearchMovie:
    def __init__(self):
        self.search_text = quote(input("请输入想要检索的关键字: "), encoding="utf-8")
        self.driver = InstantiateDriver().chrome_driver()
        self.bot = Bot()
        self.pages = Pages()

    def run_search(self):
        self.driver.get(base_url.format(self.search_text))
        pages = self.pages.get_all_pages(self.driver)
        movies = self.pages.get_all_movies(self.driver, pages)
        self.driver.quit()
        for movie in movies:
            r = requests.get(movie, headers={"user-agent": f"{user_agent}"})
            soup = bs4.BeautifulSoup(r.text, "html.parser")

            self.pages.rate_and_save(soup)
            time.sleep(5)


SearchMovie().run_search()
