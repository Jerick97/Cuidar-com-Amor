import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
