"""
Flask application to create a simple web server.
"""
import os
import logging
from flask import Flask
from dotenv import load_dotenv
from users import user_blueprint

app = Flask(__name__)
app.register_blueprint(user_blueprint)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv("../.env")

@app.route("/health")
def health():
    """
    Health check endpoint.
    """
    return "Healthy", 200

@app.route("/env")
def env():
    """
    Environment variables endpoint.
    """
    env_vars = {key: os.getenv(key) for key in os.environ.keys()}
    return env_vars, 200

@app.route("/")
def index():
    """
    Index endpoint.
    """
    return "Howdy! Neighbor Welcome to the Flask PostgreSQL App!", 200

if __name__ == "__main__":
    port = int(os.getenv("FLASK_POSTGRES_APP_PORT", "5000"))
    logger.info("Starting Flask app on port %s", port)
    app.run(host="0.0.0.0", port=port, debug=True)
