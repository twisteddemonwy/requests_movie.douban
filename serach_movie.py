import bs4
import requests


base_url = "https://search.douban.com/movie/subject_search?search_text={}"
user_agent = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

def open_url(url: str, search_text: str):
    r = requests.get(url.format(search_text))
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    return soup

def get_movie_info():
    pass


def main():
    search_text = input("请输入想要检索的关键字: ")
    soup = open_url(base_url, search_text)
    # 进入电影详细信息页面
    # 判断是否是电影，是否上映
    # 获取电影名称，一到五星数据
    # 计算电影类型
    # 将数据存入csv文件

    print(soup)


if __name__ == "__main__":
    main()
