import scrapy
from urllib.parse import urljoin


class ProductItem(scrapy.Item):
    source = scrapy.Field()
    name = scrapy.Field()
    site = scrapy.Field()
    organizer = scrapy.Field()
    date = scrapy.Field()
    Description = scrapy.Field()
    Related_industries = scrapy.Field()
    cycle = scrapy.Field()
    venue = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    logo = scrapy.Field()


class QuotesSpider(scrapy.Spider):
    name = "exhibitions"
    start_urls = [
        'https://www.eventseye.com/fairs/c1_trade-shows_poland.html',
    ]

    def parse(self, response):
        for i in response.css('table.tradeshows tr td')[::4]:
            relative_url = i.css('a::attr(href)').get()

            if relative_url and not relative_url.startswith('fairs/'):
                relative_url = 'fairs/' + relative_url

            url = urljoin('https://www.eventseye.com/fairs', relative_url)
            yield scrapy.Request(url=url, callback=self.parse_pagination)

        for i in range(2, int(response.css('div.pagenum::text').get().split('/')[-1])+1):
            next_page_url = f'https://www.eventseye.com/fairs/c1_trade-shows_poland_{i}.html'
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_pagination(self, response):
        product = ProductItem()

        product['source'] = response.url
        product['name'] = response.css('h1::text').get().replace(' 2024', '')
        product['site'] = response.css('a[rel="nofollow"]::attr(href)').get()
        product['organizer'] = response.css('a.orglink::text').get()
        product['date'] = response.css('table.dates td::text').getall()[0]
        product['Description'] = response.xpath('//div[@class="description"]//text()').getall()[-1].strip()
        product['Related_industries'] = ' | '.join(response.css('div.industries a::text').getall())
        product['cycle'] = response.xpath('//div[@class="cycle"]//text()').getall()[-1].strip()
        product['venue'] = response.css('table.dates td:nth-child(3)::text').get().strip()
        product['address'] = ' '.join([address.strip() for address in response.xpath('//div[@class="text"]/text()[preceding-sibling::br]').getall() if address.strip()])
        product['city'] = response.css('table.dates td:nth-child(2) a::text').get().strip()
        product['logo'] = urljoin('https://www.eventseye.com', response.css('img::attr(src)').get())

        yield product