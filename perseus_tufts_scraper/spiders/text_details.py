import scrapy

class TextDetailsSpider(scrapy.Spider):
    name = 'text_details'
    allowed_domains = ['tufts.edu']
    start_urls = [
        'https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0133'
    ]

    def parse(self, response):
        selector_for_links_to_word_stats = 'a.text'
        yield from response.follow_all(css=selector_for_links_to_word_stats,
                                       callback=self.parse_lexical_forms)
        
    def parse_lexical_forms(self, response):
        lexical_forms = response.css('h4.greek::text')

        if lexical_forms.get() is None:
            raise Exception(f'The word stats page {response.url!r} has no lexical forms')
        
        for lexical_form in lexical_forms.getall():
            yield {
                'lexical_form': lexical_form
            }
