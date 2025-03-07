import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
BONDS_DETAILS_FILE = os.path.join(DATA_DIR, "bonds_details_202503011115.csv")
CASHFLOWS_FILE = os.path.join(DATA_DIR, "cashflows_202503011113.csv")
COMPANY_INSIGHTS_FILE = os.path.join(DATA_DIR, "company_insights_202503011114.csv")

# Flask app configuration
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))

# Environment
ENVIRONMENT = os.getenv("FLASK_ENV", "production") 