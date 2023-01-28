import time

from locators.locators import Locators
from bot import Bot


class Pages:
    def __init__(self):
        self.bot = Bot()

    # Get the total number of pages and the url of each page (do not include the first page)
    def get_all_pages(self, driver):
        pages = int(
            self.bot.operational_elements(driver, locator=Locators.pages, index=(True, -1), attr=(False, "")).text
        )
        if not pages:
            return None

        current_url = driver.current_url
        statr = 0
        url_list = []

        for _ in range(pages - 1):
            statr += 15
            url_list.append(current_url + f"&start={statr}")

        return url_list

    # Get the urls of all movies on the current page
    def get_movie_url(self, driver):
        movies = self.bot.operational_elements(driver, locator=Locators.movies, index=(False, 0), attr=(True, "href"))

        return movies

    # Go through each page to get the url of all movies
    def get_all_movies(self, driver, pages):
        # The first page
        print(driver.current_url)
        url_list = self.get_movie_url(driver)

        # If there is more than one page, need to traverse other pages
        if pages:
            for page in pages:
                print(page)
                driver.get(page)
                url_list.extend(self.get_movie_url(driver))
                time.sleep(10)

        return url_list

    # Get movie ratings
    def get_score(self, soup):
        items = soup.select(Locators.score)
        score = [float(item.text.replace("%", "")) for item in items]

        return score

    # Director of the film
    def get_director(self, soup):
        try:
            director = soup.select(Locators.director)[0].text
            return director
        except IndexError:
            return ""

    # Rate and save
    def rate_and_save(self, soup):
        title = soup.select(Locators.title)[0].text
        print(title)

        director = self.get_director(soup)
        rate = self.get_score(soup)
        if rate:
            msg = self.rating(rate)
        else:
            msg = soup.select(Locators.no_score)[0].text.strip()
        result = {
            "电影名": title,
            "导演": director,
            "评级": f"{msg}",
        }

        self.bot.save_data_to_csv(path='result/search_result.csv', fieldnames=['电影名', '导演', '评级'], data=result)

    # Rate movies
    def rating(self, score):
        if (score[2] + score[3] + score[4]) < 10:
            msg = "F"
            return msg
        elif (score[3] + score[4]) < 10 and score[1] > score[2] and score[0] > score[2]:
            msg = "P"
            return msg
        elif score[0] < 10 and score[1] < 10 and int(score[2] + score[3]) > 20:
            msg = "b"
            return msg
        elif 70 < (score[0] + score[4]) < 80 and int(score[1] - score[4]) < 10:
            msg = "C"
            return msg
        elif score[4] > 80:
            msg = "L"
            return msg
        else:
            return "评分太过集中，无法锁定类型！！"
