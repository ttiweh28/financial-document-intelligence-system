from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")