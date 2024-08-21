from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo libro (POST)
@app.post("/libros/", response_model=schemas.Libro)
def create_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    return crud.create_libro(db=db, libro=libro)

# Ruta para obtener un libro por ID (GET)
@app.get("/libros/{libro_id}", response_model=schemas.Libro)
def read_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = crud.get_libro_by_id(db=db, libro_id=libro_id)
    if db_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return db_libro

# Ruta para actualizar un libro (PUT)
@app.put("/libros/{libro_id}", response_model=schemas.Libro)
def update_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    updated_libro = crud.update_libro(db=db, libro_id=libro_id, libro_update=libro)
    if updated_libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return updated_libro

# Ruta para eliminar un libro (DELETE)
@app.delete("/libros/{libro_id}", response_model=schemas.Libro)
def delete_libro_endpoint(libro_id: int, db: Session = Depends(get_db)):
    libro_eliminado = crud.delete_libro(db=db, libro_id=libro_id)
    if libro_eliminado is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro_eliminado