from pydantic import BaseModel

class LibroBase(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: str = None

class LibroCreate(LibroBase):
    pass

class Libro(LibroBase):
    id: int

    class Config:
        orm_mode = True
