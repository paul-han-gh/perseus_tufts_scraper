from collections.abc import Iterator

from scrapy import Spider
from scrapy.http.response import Response

from perseus_tufts_scraper.items import Book, Card


class TextStructureSpider(Spider):
    name = 'text_structure'
    allowed_domains = ['tufts.edu']
    start_urls = ['https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0133%3Abook%3D1%3Acard%3D1']

    def parse(self, response: Response) -> Iterator[Book | Card]:
        current_book_tag = (response
                            .css('div.bar')[0]
                            .css('a.current')[0])
        book_number = int(current_book_tag.attrib['title'][5:])
        percentage_of_text = float(current_book_tag.attrib['style'][7:-2])
        yield Book(text_id='1999.01.0133',
                   book_number=book_number,
                   percentage_of_text=percentage_of_text)

        for card in self._parse_cards(response, book_number):
            yield card
        
        next_book_selector = (response
                              .css('div.bar')[0]
                              .css('a.current + a'))
        if next_book_selector.get() is not None:
            next_book = next_book_selector[0]
            yield response.follow(next_book.attrib['href'], self.parse)

    def _parse_cards(self,
                     response: Response,
                     book_number: int) -> Iterator[Card]:
        card_bar = response.css('div.bar')[1]
        card_bar_parts = card_bar.css('a')
        for card_bar_part in card_bar_parts[:-1]:
            title = card_bar_part.attrib['title']
            percentage_of_book = float(card_bar_part.attrib['style'][7:-2])
            index_of_dash = title.index('-')
            first_line = int(title[6:index_of_dash])
            last_line = int(title[index_of_dash+1:])
            yield Card(text_id='1999.01.0133',
                       book_number=book_number,
                       first_line=first_line,
                       last_line=last_line,
                       percentage_of_book=percentage_of_book)
        link_to_last_card = card_bar_parts[-1].attrib['href']
        yield response.follow(url=link_to_last_card,
                              callback=self._parse_last_card_in_book,
                              cb_kwargs={'book_number': book_number})

    def _parse_last_card_in_book(self,
                                 response: Response,
                                 book_number: int) -> Iterator[Card]:
        card_bar_part = response.css('a.current')[1]
        percentage_of_book = float(card_bar_part.attrib['style'][7:-2])
        first_line = int(card_bar_part.attrib['title'][6:-3])
        labeled_lines = response.css('span.linenumber')
        last_labeled_line = labeled_lines[-1]
        last_labeled_line_number = int(
            last_labeled_line.css('span.english::text').get()
        )
        num_line_breaks_after_last_labeled_line = len(
            response.xpath('//span[@class="linenumber"][last()]/following-sibling::br')
        )
        last_line = (last_labeled_line_number
                     + num_line_breaks_after_last_labeled_line
                     - 1)
        yield Card(text_id='1999.01.0133',
                   book_number=book_number,
                   first_line=first_line,
                   last_line=last_line,
                   percentage_of_book=percentage_of_book)
