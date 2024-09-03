from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import crud, models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "hermes"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/libros/", response_model=List[schemas.Libro])
def read_libros(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    libros = crud.get_libros(db, skip=skip, limit=limit)
    return libros

@app.post("/libros/", response_model=schemas.Libro)
def create_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_admin_user)):
    return crud.create_libro(db=db, libro=libro)

