class Locators:
    # Douban
    pages = "div.paginator>a.num"
    movies = "div.item-root>a"

    # Only for single movie
    title = "h1>span:first-child"
    director = "div#info>span:first-child a"
    score = "div.ratings-on-weight span.rating_per"
    no_score = "div.rating_sum"
