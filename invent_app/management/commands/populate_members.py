from django.core.management.base import BaseCommand
from hrms.models import MCCs,MPPs,Members
import pandas as pd

class Command(BaseCommand):
    help = 'Populate sub locations data from an Excel file based on MCC CODE'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                mpp_code = row['MPP Code']
                name = row['Farmer Name']
                code = row['farmer short Code']
                max = row['Max']

                mpp, created = MPPs.objects.get_or_create(mpp_loc_code=mpp_code)

                # Create the SubLocations object
                members = Members.objects.create(
                    mpp=mpp,
                    name=name,
                    code=code,
                    max_qty = max
                )
                # Print feedback
                self.stdout.write(self.style.SUCCESS(f'Created Members: {members}'))

            self.stdout.write(self.style.SUCCESS('Members data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))
