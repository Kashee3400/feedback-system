# Generated by Django 5.0 on 2024-05-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinary', '0006_cattle_age_alter_cattle_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='price',
            new_name='normal_cost',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='case_type',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='operational_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
