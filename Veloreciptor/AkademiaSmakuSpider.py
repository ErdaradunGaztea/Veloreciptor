import scrapy
from bs4 import BeautifulSoup

from SpiderUtils import add_space_before_unit


def remove_tag(tag):
    if tag:
        return tag.group('text')


class AkademiaSmakuRecipeSpider(scrapy.Spider):
    name = 'AkademiaSmakuSpider'

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ['https://akademiasmaku.pl/przepisy/' + str(i) for i in range(int(start), int(end) + 1)]

    def parse(self, response):
        recipes = response.css('section#article.przepisy div.item > a::attr(href)').getall()
        # iterate over all collected divs with recipes on given page
        for recipe in recipes:
            yield response.follow(recipe, self.parse_recipe)

    def parse_recipe(self, response):
        preparation = response.css('section.content article > div p')
        preparation = [p for p in preparation if not p.css('p.shortdesc')]
        ingredients = response.css('div#skladniki td::text').getall()
        ingredients = [add_space_before_unit(i) for i in ingredients]

        yield {
            "link": response.url,
            "title": response.css('header.header h1::text').get(),
            "portions": BeautifulSoup(
                response.css('div.przepisy > div.info.d-flex > div > div:last-child > strong').get()
            ).text.strip().split(" ")[1],
            "photo_link": response.css('picture img::attr(src)').get(),
            "ingredients": ingredients,
            "preparation": '\n'.join([p.css('p::text').get() for p in preparation])
        }


# to call crawler use:
# scrapy runspider AkademiaSmakuSpider.py -s FEED_EXPORT_ENCODING='utf-8' -a start=1 -a end=3 -o recipes.json
