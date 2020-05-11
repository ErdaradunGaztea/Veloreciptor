import scrapy
from bs4 import BeautifulSoup


class KKPolskaRecipeSpider(scrapy.Spider):
    name = 'KKPolskaSpider'
    start_urls = ['https://kkpolska.pl/przepisy/']

    def parse(self, response):
        categories = response.css('ul#sub-navi-img > li > a::attr(href)').getall()
        # iterate over all categories of recipes
        for cat in categories:
            yield response.follow('https://kkpolska.pl/' + cat, self.parse_category)

    def parse_category(self, response):
        recipes = response.css('section.brand-teaser > ul > li > a::attr(href)').getall()
        # iterate over all recipes in category
        for recipe in recipes:
            yield response.follow('https://kkpolska.pl/' + recipe, self.parse_recipe)

    def parse_recipe(self, response):
        yield {
            "link": response.url,
            "title": response.css('article.recipe-info > header > h1::text').get(),
            "photo_link": response.css('figure.recipe > img::attr(src)').get(),
            "ingredients": response.css('section.ingredients > ul > li::text').getall(),
            "preparation": "\n".join([BeautifulSoup(p, "lxml").text for p in
                                      response.css('article.recipe-cooking > section > p').getall()])
        }


# to call crawler use:
# scrapy runspider KKPolskaSpider.py -s FEED_EXPORT_ENCODING='utf-8' -o recipes.json