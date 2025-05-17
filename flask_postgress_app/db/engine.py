"""
DB engine for Flask app with PostgreSQL.
"""

from sqlalchemy import create_engine

db_engine = create_engine(
    "postgresql+psycopg2://admin:supersecret@localhost:5432/users_database?client_encoding=utf8"
)
