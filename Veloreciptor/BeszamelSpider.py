import re

import scrapy

from SpiderUtils import add_space_before_unit


def remove_tag(tag):
    if tag:
        return tag.group('text')


class BeszamelRecipeSpider(scrapy.Spider):
    name = 'BeszamelSpider'

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ['https://beszamel.se.pl/przepisy/?page=' + str(i) for i in range(int(start), int(end) + 1)]

    def parse(self, response):
        cards = response.css('div.card')
        # iterate over all collected divs with recipes on given page
        for card in cards:
            recipe_page = card.css('a:nth-child(1)::attr(href)').get()
            yield response.follow('https://beszamel.se.pl' + recipe_page, self.parse_recipe)

    def parse_recipe(self, response):
        ingredients = response.css("div.ingredients li > p").getall()
        for index, ingredient in enumerate(ingredients):
            # removes hyperlink (if exists) and outer <p> tags from ingredient
            ingredients[index] = re.sub(r'<p>(?P<text>.*)</p>', remove_tag,
                                        re.sub(r'<a.*>(?P<text>.*)</a>', remove_tag, ingredient))
            ingredients = [add_space_before_unit(i) for i in ingredients]

        yield {
            "link": response.url,
            "title": response.css('div.title h1::text').get(),
            "portions": response.css('div.recipe-info > div.box:last-child > p > span::text').get().split(" ")[0],
            "photo_link": response.css('div.recipe-box div.img img::attr(src)').get(),
            "ingredients": ingredients,
            "preparation": '\n'.join(response.css('div.cookin li p::text').getall())
        }


# to call crawler use:
# scrapy runspider BeszamelSpider.py -s FEED_EXPORT_ENCODING='utf-8' -a start=1 -a end=1 -o recipes.json
