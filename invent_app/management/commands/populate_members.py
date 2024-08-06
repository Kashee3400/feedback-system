from django.core.management.base import BaseCommand
from vcg.models import VMPPs,VMembers
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
                # mpp_code = row['Mpp Code']
                mpp_code = row.get('Mpp Code', '')
                name = row['Farmer Name']
                code = row['farmerCode']
                max_qty = row['Max']
                cf = row['CF']
                mm = row['MM']
                mpp, created = VMPPs.objects.get_or_create(mpp_loc_code=mpp_code)
                if VMembers.objects.filter(code = code).exists():
                    vm = VMembers.objects.get(code = code)
                    vm.cattle_bag = cf
                    vm.mineral_bag = mm
                    # vm.max_qty = max_qty,
                    # vm.name = name,
                    vm.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated Members: {vm}'))
                    
                else:
                    members = VMembers.objects.create(
                        mpp=mpp,
                        name=name,
                        code=code,
                        max_qty = max,
                        cattle_bag =cf ,
                        mineral_bag= mm,
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'Created Members: {members}'))

            self.stdout.write(self.style.SUCCESS('Members data populated successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide a valid file path.'))
