from selenium import webdriver


base_url = "https://search.douban.com/movie/subject_search?search_text={}&cat=1002"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"


class InstantiateDriver:
    def chrome_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # options.add_argument(f"--proxy-server={random.choice(ip_list)}")
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        with open('stealth.min.js') as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

        driver.implicitly_wait(10)

        return driver
