from fastapi import APIRouter

from src.authors.router import router as authors_router
from src.books.router import router as books_router
from src.storing_information.router import router as storing_information_router


pre_router = APIRouter(
    prefix="/pre",
)
pre_router.include_router(authors_router)
pre_router.include_router(books_router)
pre_router.include_router(storing_information_router)
