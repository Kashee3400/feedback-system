import pandas as pd
from django.core.management.base import BaseCommand
from vcg.models import ZeroPourerMembers

class Command(BaseCommand):
    help = 'Import zero pourer members from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        
        # Load Excel file
        try:
            data = pd.read_excel(excel_file)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading Excel file: {e}"))
            return

        # Validate that the necessary columns are present
        expected_columns = ['MPP Code', 'Member Name', 'Member code']
        if not all(column in data.columns for column in expected_columns):
            self.stdout.write(self.style.ERROR(f"Missing one or more required columns: {expected_columns}"))
            return

        # Iterate over rows and create ZeroPourerMembers instances
        for index, row in data.iterrows():
            mpp = row['MPP Code']
            name = row['Member Name']
            code = row['Member code']

            try:
                ZeroPourerMembers.objects.create(mpp=mpp, name=name, code=code)
                self.stdout.write(self.style.SUCCESS(f"Successfully added: {name} - {code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to add {name} - {code}: {e}"))

        self.stdout.write(self.style.SUCCESS('Import completed successfully'))
