import scrapy
import urllib.parse


class QuotesSpider(scrapy.Spider):
    name = "wikipedia"

    start_urls = ['https://ru.wikipedia.org/wiki/Википедия:Содержание/Список_базовых_тем']

    def parse(self, response):
        for row in response.xpath("//table[@class='wide']//tr"):
            links = row.xpath(".//a/@href").extract()

            if links:
                for link in links[18:]:
                    if '.php' not in link:
                        link = urllib.parse.unquote(link)
                        yield {
                            'link': 'https://ru.wikipedia.org' + link,
                            'Subject': ' '.join(link.split('/')[-1].split('_'))
                        }

