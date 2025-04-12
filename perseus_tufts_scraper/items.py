from dataclasses import dataclass


@dataclass
class Book():
    text_id: str
    book_number: int
    percentage_of_text: float

@dataclass
class Card():
    text_id: str
    book_number: int
    first_line: int
    last_line: int
    percentage_of_book: float
