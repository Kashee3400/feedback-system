# Generated by Django 5.0 on 2024-05-09 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('veterinary', '0003_alter_member_farmerid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='FarmerId',
        ),
    ]