import os
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

notvalid_email = os.getenv('notvalid_email')
notvalid_password = os.getenv('notvalid_password')
