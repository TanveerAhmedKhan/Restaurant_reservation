import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configuration
MODEL_NAME = "gpt-4o"

# Application settings
APP_NAME = "Restaurant Chatbot"
