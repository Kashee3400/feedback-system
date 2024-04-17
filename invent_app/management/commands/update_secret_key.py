import os
from datetime import datetime, timedelta
import secrets
import string
from django.core.management.base import BaseCommand
from dotenv import load_dotenv,set_key

load_dotenv()

class Command(BaseCommand):
    help = 'Updates the SECRET_KEY environment variable if expired'

    def generate_secret_key(self, length=50):
        """
        Generate a random secret key.

        Args:
            length (int): Length of the secret key (default is 50 characters).

        Returns:
            str: Random secret key.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        secret_key = ''.join(secrets.choice(characters) for _ in range(length))
        return secret_key

    def is_secret_key_expired(self, timestamp_str):
        """
        Check if the secret key has expired.

        Args:
            timestamp_str (str): Timestamp string in ISO format.

        Returns:
            bool: True if the secret key has expired, False otherwise.
        """
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str)
            current_time = datetime.now()
            return current_time - timestamp > timedelta(days=3)
        else:
            return False

    def handle(self, *args, **options):
        secret_key_timestamp = os.getenv('SECRET_KEY_TIMESTAMP', None)
        if self.is_secret_key_expired(secret_key_timestamp):
            new_secret_key = self.generate_secret_key()
            
            set_key('.env', 'SECRET_KEY', new_secret_key)
            set_key('.env', 'SECRET_KEY_TIMESTAMP', datetime.now().isoformat())

            self.stdout.write(self.style.SUCCESS('Updated SECRET_KEY'))
        else:
            self.stdout.write(self.style.SUCCESS('SECRET_KEY is up to date'))
