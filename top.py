import bs4
import csv
import requests

from time import sleep


base_url = "https://movie.douban.com/top250"
user_agent = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
# proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
fieldnames = ['title', 'score', 'num_of_people', 'playback_addresses']


def open_url(url):
    # r = requests.get(url, headers=headers, proxies=proxies)
    r = requests.get(url, headers=user_agent)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    return soup

def get_all_pages(soup):
    url_list = [""]
    pages = soup.select("div.paginator>a")
    for page in pages:
        url = base_url + page.attrs["href"]
        url_list.append(url)

    return url_list


def get_movie_info(movie):
    href = movie.div.a.attrs["href"]
    movie_r = requests.get(href, headers=user_agent)

    return bs4.BeautifulSoup(movie_r.text, "html.parser")


def get_playback_addresses(movie):
    playback_addresses = ""
    movie_soup = get_movie_info(movie)
    addresses = movie_soup.find_all("a", class_="playBtn")
    for address in addresses:
        platform = address.text.strip()
        link = address.attrs["href"].strip()
        playback_addresses = playback_addresses + platform + ": " + link + "\n"

    return {"playback_addresses": playback_addresses}


def get_movie_score(movie):
    title = movie.div.a.span.text
    score = movie.select("span.rating_num")[0].text
    num_of_people = movie.select("div.star span:last-child")[0].text

    return {"title": title, "score": score, "num_of_people": num_of_people}


def main():
    soup = open_url(base_url)
    all_pages = get_all_pages(soup)

    with open('movie.csv', 'a') as f:
        csvw = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        csvw.writeheader()

        for page in all_pages:
            if page:
                soup = open_url(page)
            movies = soup.find_all("div", class_="info")
            for movie in movies:
                movie_info = get_movie_score(movie)
                movie_info.update(get_playback_addresses(movie))
                csvw.writerows([movie_info])
                sleep(3)


if __name__ == "__main__":
    main()
