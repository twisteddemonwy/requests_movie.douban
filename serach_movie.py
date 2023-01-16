import bs4
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote


base_url = "https://search.douban.com/movie/subject_search?search_text={}&cat=1002"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

class locators:
    pages = "div.paginator>a.num"
    movies = "div.item-root>a"
    title = "h1>span:first-child"
    director = "div#info>span:first-child a"
    score = "div.ratings-on-weight span.rating_per"
    number_of_evaluations = "div.rating_sum span"


def configure_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    with open('stealth.min.js') as f:
        js = f.read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    driver.implicitly_wait(10)

    return driver


def open_url():
    # 转换字符
    search_text = quote(input("请输入想要检索的关键字: "), encoding="utf-8")

    driver = configure_driver()
    driver.get(base_url.format(search_text))

    return driver


# 获取搜索结果页数，及各页url
def get_all_pages(driver):
    try:
        pages = int(driver.find_elements(by=By.CSS_SELECTOR, value=locators.pages)[-1].text)
    except IndexError:
        return None
    current_url = driver.current_url
    statr = 0
    url_list = []
    for _ in range(pages-1):
        statr += 15
        url_list.append(current_url + f"&start={statr}")

    return url_list


# 获取当前页面所有电影的url
def get_movie_url(driver):
    movie_list = []
    movies = driver.find_elements(by=By.CSS_SELECTOR, value=locators.movies)
    for movie in movies:
        movie_list.append(movie.get_attribute("href"))

    return movie_list


# 获取当前关键词下所有电影的url
def get_all_movies(driver, pages):
    # 第一页
    url_list = get_movie_url(driver)

    # 如果有其他页，需要打开每一页获取url
    if pages:
        for page in pages:
            driver.get(page)
            url_list.extend(get_movie_url(driver))

    return url_list


# 获取当前电影的评分
def get_score(movie_info):
    print(movie_info.select(locators.title)[0].text)

    score = []
    items = movie_info.select(locators.score)
    for i in items:
        score.append(i.text.replace("%", ""))

    return score




def main():
    no_score = []

    driver = open_url()
    pages = get_all_pages(driver)
    movies = get_all_movies(driver, pages)
    driver.quit()

    for i in movies:
        r = requests.get(i, headers={"user-agent": f"{user_agent}"})
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        score = get_score(soup)
        print(score)

    # 获得电影的评分
    # 如果不存在评分 判断是否为未上映，做存储
    # 如果存在评分，判断评级


if __name__ == "__main__":
    main()
