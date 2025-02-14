from os import getenv

from .base import *
from .base import BASE_DIR

env_file = path.join(BASE_DIR, "env", ".env.dev")
if path.isfile(env_file):
    load_dotenv(dotenv_path=env_file)

DEBUG = True

SITE_NAME = getenv("SITE_NAME")
SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY",
    "8k0n2u663u9-fO5v4nZ6p-Habf4lJdcVgSi-W-XRzTStR6EV_xs",
)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

ADMIN_URL = getenv("DJANGO_ADMIN_URL")
DOMAIN = getenv("DOMAIN")
