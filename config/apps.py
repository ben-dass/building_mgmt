import logging

from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class ConfigAppConfig(AppConfig):
    name = "config"

    def ready(self):
        self.check_database_connection()

    @staticmethod
    def check_database_connection():
        """Check if the database connection is successful."""
        try:
            connection = connections["default"]
            connection.cursor()
            logger.info("Successfully connected to the database.")
        except OperationalError:
            logger.error("Database connection failed!")
