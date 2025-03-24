import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")


if not Config.OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is missing!")
