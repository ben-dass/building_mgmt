from os import getenv, path

from dotenv import load_dotenv

from .base import BASE_DIR

env_file = path.join(BASE_DIR, ".env", ".env.dev")
if path.isfile(env_file):
    load_dotenv(dotenv_path=env_file)

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

ADMIN_URL = getenv("DJANGO_ADMIN_URL")

# When Debug is set to false, the following list of emails will be contact with errors/exceptions.
ADMINS = [
    ("Benjamin Dass", "bdas16001@gmail.com"),
]
