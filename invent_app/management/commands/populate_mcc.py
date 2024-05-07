from django.core.management.base import BaseCommand
from vcg.models import VMCCs
import pandas as pd

class Command(BaseCommand):
    help = 'Populate location data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                mcc_code = row['MCC CODE']
                mcc = row['MCC']

                # Check if a record with the given mcc_code already exists
                try:
                    location = VMCCs.objects.get(mcc_code=mcc_code)
                    location.mcc = mcc  # Update mcc field
                    location.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated Location: {location}'))
                except VMCCs.DoesNotExist:
                    # If the record doesn't exist, create it
                    location = VMCCs.objects.create(mcc_code=mcc_code, mcc=mcc)
                    self.stdout.write(self.style.SUCCESS(f'Created Location: {location}'))

            self.stdout.write(self.style.SUCCESS('Location data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))
