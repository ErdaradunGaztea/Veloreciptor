import re

import scrapy


def remove_tag(tag):
    if tag:
        return tag.group('text')


class PolkiRecipeSpider(scrapy.Spider):
    """Unfinished spider"""
    name = 'PolkiSpider'

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ['https://polki.pl/tagi,przepisy-kulinarne,54851,{0}.html'.format(i)
                           for i in range(int(start), int(end) + 1)]

    def parse(self, response):
        # collect all cards with articles
        cards = response.css('div.content-list > div.medium-up-3 > div')
        # remove articles from partners
        cards = [card for card in cards if not card.css('div.partner')]
        # iterate over all collected divs with recipes on given page
        for card in cards:
            yield response.follow(card.css('a::attr(href)').get(), self.parse_recipe)

    def parse_recipe(self, response):
        # select divs which MAY contain ingredients
        ingredient_divs = response.css('div.recipe-box > div.components')
        # filter divs
        ingredient_divs = [div for div in ingredient_divs if div.css('h5::text').get() == 'Składniki:']
        # continue only if there is a div with ingredients
        if ingredient_divs:
            yield {
                "link": response.url,
                "title": response.css('div.title h1::text').get(),
                "photo_link": response.css('article.article picture img::attr(src)').get(),
                "ingredients": ingredient_divs[0].css('ul > li').getall(),
                "preparation": '\n'.join(response.css('div.cookin li p::text').getall())
            }


# to call crawler use:
# scrapy runspider [deprecated]PolkiSpider.py -s FEED_EXPORT_ENCODING='utf-8' -a start=1 -a end=1 -o recipes.json
