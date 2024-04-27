# your_app/management/commands/populate_month_assignment.py

import pandas as pd
from django.core.management.base import BaseCommand
from invent_app.models import MonthAssignment,VMPPs

class Command(BaseCommand):
    help = 'Populate MonthAssignment model with data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to Excel file')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file)
            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                mpp_code = row['MPP Code']
                if VMPPs.objects.filter(mpp_loc_code=str(int(mpp_code))).exists():
                    mpp = VMPPs.objects.get(mpp_loc_code=str(int(mpp_code)))
                    month_assignment = MonthAssignment.objects.create(
                        mpp = mpp,
                        milk_collection=row['LTS Per Day'],
                        no_of_members=row['No Of Members'],
                        no_of_pourers=row['No Of Pourers'],
                        pourers_15_days=row['15 Days Pourer'],
                        pourers_25_days=row['25 Days Pourer'],
                        zero_days_pourers=row['Zero Days Pourer'],
                        cattle_feed_sale=row['Cattle Feed Sale Member'],
                        mineral_mixture_sale=row['Mineral Sale Member'],
                        sahayak_recovery=row['Sahayak Recovery']
                    )
                    month_assignment.save()
                    self.stdout.write(self.style.SUCCESS('Data populated successfully'))
                else:
                    self.stdout.write(self.style.ERROR(f'Mpp {str(int(mpp_code))} not exists'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
