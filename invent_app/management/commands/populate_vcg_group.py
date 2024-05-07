import pandas as pd
from django.core.management.base import BaseCommand
from vcg.models import VCGroup, VMembers

class Command(BaseCommand):
    help = 'Populate VCGroup model from Excel sheet'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Read Excel file
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading Excel file: {e}"))
            return

        # Iterate through rows and create VCGroup instances
        for index, row in df.iterrows():
            # whatsapp_num = row['Whatsapp Number']
            code = row['Code']
            member, created = VMembers.objects.get_or_create(code=code)
            vcgroup = VCGroup.objects.create(member=member)
            self.stdout.write(self.style.SUCCESS(f"Successfully created VCGroup: {vcgroup}"))
