from django.core.management.base import BaseCommand
from hrms.models import MCCs
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
                mcc_code = row['MCC Code']
                mcc = row['mccName']

                # Create or update the Location object
                location, created = MCCs.objects.update_or_create(
                    mcc_code=mcc_code,
                    defaults={'mcc': f'MCC/Plant - {mcc}'}
                )

                # Print feedback
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Location: {location}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated Location: {location}'))

            self.stdout.write(self.style.SUCCESS('Location data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))


