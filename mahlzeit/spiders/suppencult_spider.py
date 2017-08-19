import scrapy
from mahlzeit.items import create_dish_for_week
from mahlzeit.items import get_monday_date


def delete_idexes(elements, idexes):
    counter = 0
    for idx in idexes:
        index = idx - counter
        del elements[index]
        counter += 1


class SuppenCultSpider(scrapy.Spider):
    name = "suppencult"
    start_urls = ['http://suppen-cult.de/index.php?page=8']
    business = 'Suppencult'
    location = 'Alexanderplatz'

    def parse(self, response):
        names = response.xpath('//div[@class="suppe_name"]/text()').extract()
        prices = response.xpath('//div[@class="suppe_preis"]/text()').extract()
        dishes = response.xpath('//div[@class="suppe_zutaten"]/text()').extract()
        #vegetarian = response.xpath('/body/content/div[@id="background"]/div[@id="page"]/div[@id="content"]/div[@id="wochenkarte"]')
        #vegetarian = response.xpath('//div[@id="background"]/div[@id="page"]/div[@id="content"]/div[@id="pagecontent"]/div[@class="suppe_zutaten"]/text()').extract()

        # delete invalid dishes descriptions
        idxs = list()
        for i in range(len(dishes)):
            if 'An heißen Sommertagen'.lower() in dishes[i].lower():
                idxs.append(i)
            elif 'Unsere vegetarischen Suppen'.lower() in dishes[i].lower():
                idxs.append(i)
            elif 'geschlossen' in dishes[i]:
                idxs.append(i)
        delete_idexes(dishes, idxs)
        # delete invalid titles
        idxs = list()
        for i in range(len(names)):
            if 'schließzeiten' in names[i].lower():
                idxs.append(i)
        delete_idexes(names, idxs)

        if len(names) != len(dishes) or len(names) != len(prices):
            raise KeyError('prices and dishes have different length')

        result = list()
        date = get_monday_date()
        for title, price, dish in zip(names, prices, dishes):
            dish = title + ' ' + dish
            result.extend(create_dish_for_week(self.location, self.business, dish, date, list(), price))

        return result
