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


class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True