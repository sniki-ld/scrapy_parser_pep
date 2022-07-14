import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Парсер ссылок на страницы Pep."""
        tbody = response.css('tbody')

        for tr in tbody.css('tr'):
            link_pep_page = tr.css('td').css('a::attr(href)').get()
            if link_pep_page is not None:
                yield response.follow(link_pep_page, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсер персональной страницы Pep."""
        title = response.css('h1.page-title::text').get()

        data = {
            'number': [int(s) for s in title.split() if s.isdigit()][0],
            'name': title,
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
