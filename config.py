import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "wildlife-habitat-secret-key"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    RESULT_FOLDER = os.path.join(BASE_DIR, "static", "results")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
