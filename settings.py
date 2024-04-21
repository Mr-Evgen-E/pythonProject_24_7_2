import os
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv("valid_email")
valid_password = os.getenv("valid_password")

not_valid_email = os.getenv("not_valid_email")
not_valid_password = os.getenv("not_valid_password")

empty_email = os.getenv("empty_email")
empty_password = os.getenv("empty_password")
