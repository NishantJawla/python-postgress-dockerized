"""
user views module
"""

import logging
from http import HTTPStatus
from faker import Faker
from flask import Blueprint, Response
from sqlalchemy import text
from db import db_engine


logger = logging.getLogger(__name__)
faker = Faker("en_US")
user_blueprint = Blueprint("user", __name__, url_prefix="/user")

@user_blueprint.route("/")
def index():
    """
    User index page.
    """
    return Response(
        "User index page",
        status=HTTPStatus.OK,
    )

@user_blueprint.route("/create/<int:user_count>")
def create_user(user_count):
    """
    Create a new user and insert into the database.
    """
    if db_engine is None:
        logger.error("Database engine is not initialized.")
        return Response(
            "Database connection error",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    with db_engine.connect() as connection:
        transaction = connection.begin()  # Start a transaction
        try:
            for i in range(user_count):
                username = faker.user_name()
                email = faker.email()
                password_hash = faker.password(length=12)

                # Insert user data into the database
                query = text("""
                    INSERT INTO users (username, email, password_hash)
                    VALUES (:username, :email, :password_hash)
                """)
                connection.execute(query, {
                    "username": username,
                    "email": email,
                    "password_hash": password_hash
                })
                logger.info("User %d created: %s, %s", i + 1, username, email)

            transaction.commit()  # Commit the transaction
        except Exception as e:
            transaction.rollback()  # Rollback the transaction on error
            logger.error("Error creating users: %s", str(e))
            return Response(
                "Failed to create users",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    return Response(
        f"{user_count} users created and inserted into the database",
        status=HTTPStatus.CREATED,
    )
