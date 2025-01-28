books = [
    {
        "id": 1,
        "title": "Python Tricks: The Book",
        "author": "Dan Bader",
        "publisher": "Dan Bader",
        "published_date": "2017-10-01",
        "page_count": 302,
        "language": "English",
    },
    {
        "id": 2,
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-01",
        "page_count": 464,
        "language": "English",
    },
    {
        "id": 3,
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "publisher": "No Starch Press",
        "published_date": "2015-04-14",
        "page_count": 504,
        "language": "English",
    },
    {
        "id": 4,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "publisher": "Addison-Wesley",
        "published_date": "1999-10-20",
        "page_count": 352,
        "language": "English",
    },
    {
        "id": 5,
        "title": "You Don't Know JS: Scope & Closures",
        "author": "Kyle Simpson",
        "publisher": "O'Reilly Media",
        "published_date": "2014-12-01",
        "page_count": 98,
        "language": "English",
    },
    {
        "id": 6,
        "title": "Fluent Python",
        "author": "Luciano Ramalho",
        "publisher": "O'Reilly Media",
        "published_date": "2015-08-20",
        "page_count": 792,
        "language": "English",
    },
]

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


@app.get('/books', response_model=List[Book])
async def get_all_books() -> list:
    return books


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book


@app.get('/book/{book_id}')
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found.")


@app.patch('/book/{book_id}')
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found.")



@app.delete('/book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found.")