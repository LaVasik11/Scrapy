import scrapy


class QuotesSpider(scrapy.Spider):
    name = "goods"
    categories = ['vintage', 'home-and-living', 'clothing', 'electronics-and-accessories', 'shoes',
                  'art-and-collectibles', 'paper-and-party-supplies', 'accessories', 'weddings',
                  'toys-and-games', 'bath-and-beauty', 'jewelry', 'bags-and-purses',
                  'pet-supplies', 'books-movies-and-music', 'craft-supplies-and-tools']
    start_urls = [f'https://www.etsy.com/c/{i}' for i in categories]

    def parse(self, response):
        for i in response.css('ol.wt-grid.wt-grid--block.wt-pl-xs-0.tab-reorder-container li'):
            free_shipping_text = i.css('span.wt-badge.wt-badge--small.wt-badge--statusValue::text').get(default="").strip()
            free_shipping = free_shipping_text.lower() == "free shipping"

            yield {
                'name': i.css("h3::text").get().strip(),
                'price': i.css("span.currency-value::text").get().strip() + i.css("span.currency-symbol::text").get(),
                'free shipping': free_shipping,
                'link': i.css("a.listing-link.wt-display-inline-block::attr(href)").get()
            }

        next_page = response.css('ul.wt-action-group.wt-list-inline li.wt-action-group__item-container:last-child a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)