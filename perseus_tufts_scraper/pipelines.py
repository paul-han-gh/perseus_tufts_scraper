from dataclasses import asdict

from scrapy.exporters import JsonLinesItemExporter

from perseus_tufts_scraper.items import Book, Card


class TextStructurePipeline:
    def open_spider(self, spider):
        self.book_exporter = JsonLinesItemExporter(open('books.jsonl', 'wb'))
        self.card_exporter = JsonLinesItemExporter(open('cards.jsonl', 'wb'))
        
        self.book_exporter.start_exporting()
        self.card_exporter.start_exporting()

    def close_spider(self, spider):
        self.book_exporter.finish_exporting()
        self.card_exporter.finish_exporting()

    def process_item(self, item, spider):
        if isinstance(item, Book):
            self.book_exporter.export_item(asdict(item))
        elif isinstance(item, Card):
            self.card_exporter.export_item(asdict(item))
        return item
