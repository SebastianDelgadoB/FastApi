from sqlalchemy.orm import Session
import models, schemas

def create_libro(db: Session, libro: schemas.LibroCreate):
    db_libro = models.Libro(
        titulo=libro.titulo,
        autor=libro.autor,
        paginas=libro.paginas,
        editorial=libro.editorial
    )
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def get_libro_by_id(db: Session, libro_id: int):
    return db.query(models.Libro).filter(models.Libro.id == libro_id).first()

def update_libro(db: Session, libro_id: int, libro_update: schemas.LibroCreate):
    db_libro = get_libro_by_id(db, libro_id)
    if not db_libro:
        return None
    
    # Actualizar los campos del libro
    db_libro.titulo = libro_update.titulo
    db_libro.autor = libro_update.autor
    db_libro.paginas = libro_update.paginas
    db_libro.editorial = libro_update.editorial
    
    db.commit()
    db.refresh(db_libro)
    return db_libro

def delete_libro(db: Session, libro_id: int):
    # Buscar el libro por su ID
    db_libro = get_libro_by_id(db, libro_id)
    
    # Si el libro no existe, retornar None o lanzar una excepción si prefieres
    if not db_libro:
        return None
    
    # Eliminar el libro de la base de datos
    db.delete(db_libro)
    db.commit()
    
    # Retornar el libro eliminado, o simplemente un mensaje de éxito
    return db_libro
