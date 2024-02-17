from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from src.core.db.models import Base


class Author(Base):
    __tablename__ = "author"

    key = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author")

# class Book(Base):
#     __tablename__ = "book"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     publish_year = Column(Integer, nullable=False)
#     barcode = Column(String, nullable=False, unique=True)
#     author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

#     author = relationship("Author", back_populates="books")
#     storing_information = relationship("StoringInformation", back_populates="book")

# class StoringInformation(Base):
#     __tablename__ = "storing_information"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     date = Column(Date, nullable=False)

#     book = relationship("Book", back_populates="storing_information")
