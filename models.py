from sqlalchemy import Column, Integer, String
from database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String)
    paginas = Column(Integer)
    editorial = Column(String, nullable=True)
