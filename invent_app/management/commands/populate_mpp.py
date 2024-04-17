from django.core.management.base import BaseCommand
from hrms.models import MCCs,MPPs
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
                mcc_code = row['MCC Code']
                mpp_name = row['MPP Nmae']
                mpp_code = row['MPP Code']

                # Get or create the Location object based on the mcc_code
                mcc, created = MCCs.objects.get_or_create(mcc_code=mcc_code)

                # Create the SubLocations object
                sub_location = MPPs.objects.update_or_create(
                    mcc=mcc,
                    mpp_loc=mpp_name,
                    mpp_loc_code=mpp_code
                )

                # Print feedback
                self.stdout.write(self.style.SUCCESS(f'Created Sub Location: {sub_location}'))

            self.stdout.write(self.style.SUCCESS('Sub locations data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))
