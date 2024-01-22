import scrapy
from urllib.parse import urljoin
import re


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    Manufacturer = scrapy.Field()


class QuotesSpider(scrapy.Spider):
    name = "vektor-iz"

    start_urls = [
            'https://vektor-iz.ru/#',
        ]

    def parse(self, response):
        category_links = response.css('a.btn.btn--transparent.btn--extra-small-width::attr(href)').extract()

        for category_link in category_links:
            full_category_url = urljoin('https://vektor-iz.ru/', category_link)
            yield scrapy.Request(url=full_category_url, callback=self.parse_category)

    def parse_category(self, response):
        last_page_number = int(response.css('div.pagination a::text').getall()[-1])
        category_link = response.url
        for i in range(1, last_page_number + 1):
            full_pagination_url = f'{category_link}?PAGEN_1={i}'
            yield scrapy.Request(url=full_pagination_url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        product_links = response.css('a.product-item__btn-detail::attr(href)').extract()

        for product_link in product_links:
            full_product_url = urljoin('https://vektor-iz.ru/', product_link)
            yield scrapy.Request(url=full_product_url, callback=self.parse_product)


    def parse_product(self, response):

        product = ProductItem()
        product['name'] = response.css('div.product-detail__title::text').get().replace('\t', '').strip()
        price_with_symbols = response.css('div.product-detail__price span::text').get().strip()
        product['price'] = self.extract_digits(price_with_symbols) if price_with_symbols else "Цена по запросу"

        product['in_stock'] = response.css('span.product-status.product-status--instock::text').get()
        if product['in_stock']:
            product['in_stock'] = product['in_stock'].strip()
        else:
            product['in_stock'] = "Нет в наличии"

        manufacturer_elements = response.css('div.product-detail__sku::text').getall()
        if manufacturer_elements:
            product['Manufacturer'] = manufacturer_elements[-1].strip().split('Производитель: ')[-1]
        else:
            product['Manufacturer'] = "Неизвестно"

        yield product

    def extract_digits(self, text):
        return ''.join(char for char in text if char.isdigit())



