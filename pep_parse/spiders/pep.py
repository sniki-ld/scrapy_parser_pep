import scrapy
# from urllib.parse import urljoin

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        # section_tag = response.css('section[id=numerical-index]')
        tbody = response.css('tbody')
        # tr_tags = tbody.css('tr')

        for tr in tbody.css('tr'):
            # в тегах td найти ссылку a на стр рер
            link_pep_page = tr.css('td').css('a::attr(href)').get()
            # path_pep = urljoin(PepSpider.start_urls[0], link_pep_page)
            if link_pep_page is not None:
                yield response.follow(link_pep_page, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()

        data = {
            # 'number': int(title[:title.find(' –')].replace('PEP ', ''))
            'number': [int(s) for s in title.split() if s.isdigit()][0],
            'name': title,
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
