from database import engine, Base
from models import Libro

# Aqui creamos todas las tablas definidas en la Base de datos

Base.metadata.create_all(bind=engine)

print("Base de datos y tablas creadas con éxito.")
