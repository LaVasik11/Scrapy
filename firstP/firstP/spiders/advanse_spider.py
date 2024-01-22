import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "advance"

    lime_server = ['https://forum.advance-rp.ru/forums/zhaloby-na-administraciju.578/',
                  'https://forum.advance-rp.ru/threads/lime-o-zhaloby-na-igrokov-sostojaschix-v-gos-organizacijax.2440356/,',
                  'https://forum.advance-rp.ru/threads/lime-o-zhaloby-na-igrokov-ne-sostojaschix-v-organizacijax.2440358/',
                  'https://forum.advance-rp.ru/threads/lime-o-zhaloby-na-igrokov-oos-meroprijatija-bitva-za-kejs-family.2257143/',
                  'https://forum.advance-rp.ru/threads/lime-o-zhaloby-na-banditov.2471306/',
                  'https://forum.advance-rp.ru/threads/lime-o-zhaloby-na-sostojaschix-v-min-justicii-mvd.2440360/',
                  'https://forum.advance-rp.ru/forums/zhaloby-na-liderov-organizacij.620/'
                  ]
    green_server = ['https://forum.advance-rp.ru/forums/zhaloby-na-administraciju.58/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-banditov.2508527/',
                    'https://forum.advance-rp.ru/forums/zhaloby-na-liderov-organizacij.618/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-uchastnikov-bitv-za-kejsy.2195215/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-sostojaschix-v-mo.2375860/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-sostojaschix-v-mju.2375859/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-ne-sostojaschix-v-organizacii.2375862/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-sostojaschix-v-smi.2375864/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-sostojaschix-v-pravitelstve.2375863/',
                    'https://forum.advance-rp.ru/threads/green-zhaloby-na-sostojaschix-v-mz.2375865/',
                    ]
    blue_server = ['https://forum.advance-rp.ru/forums/zhaloby-na-administraciju.213/',
                  'https://forum.advance-rp.ru/forums/zhaloby-na-liderov-organizacij.619/',
                  'https://forum.advance-rp.ru/threads/blue-zhaloby-na-igrokov-ne-sostojaschix-v-organizacijax.2517081/',
                  'https://forum.advance-rp.ru/threads/blue-zhaloby-na-igrokov-gosudarstvennyx-organizacij.2513070/',
                  'https://forum.advance-rp.ru/threads/blue-zhaloby-na-igrokov-sostojaschix-v-mafijax.2494295/',
                  ]
    red_server = ['https://forum.advance-rp.ru/forums/zhaloby-na-administraciju.15/',
                  'https://forum.advance-rp.ru/forums/zhaloby-na-liderov-organizacij.617/',
                  'https://forum.advance-rp.ru/threads/red-server-zhaloby-na-banditov.2469753/',
                  'https://forum.advance-rp.ru/threads/red-server-zhaloby-na-igrokov-ne-sostojaschix-v-organizacii.2466167/',
                  'https://forum.advance-rp.ru/threads/red-server-zhaloby-na-mafiozi.2464733/',
                  'https://forum.advance-rp.ru/threads/red-server-zhaloby-na-igrokov-gosudarstvennyx-organizacij.2515105/',
                  'https://forum.advance-rp.ru/threads/red-server-zhaloby-na-narushenija-pravil-so-storony-mvd.2464578/',
                  'https://forum.advance-rp.ru/threads/red-server-zhaloby-na-partii-i-narushenija-vo-vremja-vyborov.1178775/']

    all_servers = lime_server + green_server + red_server + blue_server

    start_urls = all_servers

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.user_count = {}

    def parse(self, response):
        for i in response.css("a.username"):
            username = i.xpath('text()').get()
            if username:
                self.user_count[username] = self.user_count.get(username, 0) + 1

        next_page = response.css('a.pageNav-jump.pageNav-jump--next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def closed(self, reason):
        sorted_user_count = dict(sorted(self.user_count.items(), key=lambda x: x[1], reverse=True))
        with open('advance.json', 'w', encoding='utf-8') as json_file:
                        json.dump(sorted_user_count, json_file, ensure_ascii=False, indent=4)



