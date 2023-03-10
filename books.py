import uuid
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, fields

app = FastAPI()


class BooksModels(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]


BOOKS = {
    "book_1": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "book_2": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "book_3": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "book_4": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "book_5": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},

}


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.post("/books/")
async def use_pydantic(baseModel: BooksModels):
    return baseModel


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split("_")[-1])
            if x > current_book_id:
                current_book_id = x

    BOOKS[f"book_{current_book_id + 1}"] = {"title": book_title, "author": book_author}
    return BOOKS[f"book_{current_book_id + 1}"]


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_information
    return book_information


@app.delete("/{book_name}")
async def delete_book(book_name):
    del BOOKS[book_name]
    return f"Book {book_name} deleted."
