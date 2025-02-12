from typing import Dict, List
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre, InMemoryDB
import json

router = APIRouter()
db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

def format_response(content):
    """Helper function to format JSON response with proper indentation"""
    return json.loads(json.dumps(content, indent=2))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=format_response(book.model_dump())
    )

@router.get("/", status_code=status.HTTP_200_OK)
async def get_books() -> List[Dict]:
    books = db.get_books()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=format_response([book.model_dump() for book in books.values()])
    )

@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=format_response(book.model_dump())
    )

@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book):
    updated_book = db.update_book(book_id, book)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=format_response(updated_book.model_dump())
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
