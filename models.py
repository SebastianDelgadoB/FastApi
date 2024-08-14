# models.py
from sqlalchemy import Table, Column, Integer, String
from .database import metadata

# Definimos un modelo simple
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(100), unique=True),
)
