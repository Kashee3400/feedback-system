from django.core.management.base import BaseCommand
from vcg.models import VMCCs,Facilitator
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

            # Initialize a dictionary to store unique names for each MCC code
            unique_names = {}

            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                mcc_code = row['MCC Code']
                name = row['FS Name']

                # Check if the name is already added for the current MCC code
                if name not in unique_names.get(mcc_code, set()):
                    mcc, created = VMCCs.objects.get_or_create(mcc_code=mcc_code)
                    facilitator, created = Facilitator.objects.update_or_create(
                        mcc=mcc,
                        name=name,
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created Facilitator: {facilitator}'))

                    # Add the name to the set of unique names for the current MCC code
                    unique_names.setdefault(mcc_code, set()).add(name)
                else:
                    self.stdout.write(self.style.WARNING(f'Duplicate entry for MCC code {mcc_code} and name {name}. Skipping...'))

            self.stdout.write(self.style.SUCCESS('Facilitator data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))
