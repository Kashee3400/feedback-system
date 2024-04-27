from django.db import IntegrityError  # Import IntegrityError
from django.core.management.base import BaseCommand
from invent_app.models import VMCCs, VMPPs
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
                district = row['District Name']

                # Get or create the Location object based on the mcc_code
                mcc, created = VMCCs.objects.get_or_create(mcc_code=mcc_code)

                try:
                    # Try to create the SubLocations object
                    sub_location, created = VMPPs.objects.get_or_create(
                        mcc=mcc,
                        mpp_loc=mpp_name,
                        mpp_loc_code=mpp_code,
                        district=district
                    )
                    # Print feedback
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created VMPP: {sub_location}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'SubLocation already exists: {sub_location}'))
                except IntegrityError:
                    # Handle IntegrityError (duplicate entry) and continue with the next iteration
                    self.stdout.write(self.style.WARNING(f'Duplicate entry encountered for MCC {mcc_code}, skipping...'))
                    continue

            self.stdout.write(self.style.SUCCESS('MPP data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))
