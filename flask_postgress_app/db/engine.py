"""
DB engine for Flask app with PostgreSQL.
"""
import os
import logging
from sqlalchemy import create_engine

# Set up logging
logger = logging.getLogger(__name__)

postgres_user = os.getenv("POSTGRES_USER", "")
postgres_password = os.getenv("POSTGRES_PASSWORD", "")
postgres_host = os.getenv("POSTGRES_HOST", "")
postgres_db = os.getenv("POSTGRES_DB", "")

logger.info("Postgres user: %s", postgres_user)
logger.info("Postgres password: %s", postgres_password)
logger.info("Postgres host: %s", postgres_host)
logger.info("Postgres db: %s", postgres_db)

# use the above variables to create the connection string
db_engine = None

while True:
    try:
        # Create the database engine
        db_url = (
            f"postgresql+psycopg2://{postgres_user}:{postgres_password}"
            f"@{postgres_host}:5432/{postgres_db}?client_encoding=utf8"
        )
        logger.info("Database URL: %s", db_url)
        db_engine = create_engine(db_url)
        # Test the connection
        with db_engine.connect() as connection:
            logger.info("Successfully connected to the PostgreSQL database.")
        break  # Exit the loop if the connection is successful
    except Exception as e:
        logger.error("Error connecting to PostgreSQL database: %s", e)
        break  # Exit the loop if the connection fails
