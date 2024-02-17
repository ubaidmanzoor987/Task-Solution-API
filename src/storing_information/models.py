from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.core.db.models import Base


class StoringInformation(Base):
    __tablename__ = "storing_information"

    key = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("book.key"), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=True)

    book = relationship("Book", back_populates="storing_information")
