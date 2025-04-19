from dotenv import load_dotenv
import os
load_dotenv()
LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASS")
OPENAI_KEY = os.getenv("OPENAI_KEY")
# ... etc.
