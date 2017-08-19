from scrapy.spiders import CSVFeedSpider
from mahlzeit.items import MenuItem


class JouisNourSpider(CSVFeedSpider):
    name = "jouisnour"
    start_urls = ['file:///home/frevilla/devel/scrapy/mahlzeit/data/jouisnour.csv']
    headers = ['date', 'location', 'business', 'price', 'type', 'name']
    delimiter = ';'

    def parse_row(self, response, row):
        # skip headers
        if row['date'] == 'date' and row['location'] == 'location':
            return
        # extract ingredients
        types = row['type']
        types = types.split(',')
        ingredients = list()
        for t in types:
            t = t.replace(' ', '')
            if len(t) > 1:
                ingredients.append(t.replace(' ', ''))
        # create item
        item = MenuItem()
        item['date'] = row['date']
        item['location'] = row['location']
        item['business'] = row['business']
        item['price'] = row['price']
        item['dish'] = row['name']
        item['ingredients'] = ingredients
        return item
