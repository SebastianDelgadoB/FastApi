# database.py
from sqlalchemy import create_engine, MetaData
from databases import Database

# URL de la base de datos; SQLite en este caso
DATABASE_URL = "sqlite:///./test.db"

# Si usás PostgreSQL o MySQL, la URL sería algo así:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Configuramos la conexión
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Métodos para conectar y desconectar la base de datos
async def connect():
    await database.connect()

async def disconnect():
    await database.disconnect()
