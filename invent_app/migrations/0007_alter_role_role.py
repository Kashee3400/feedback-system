# Generated by Django 5.0 on 2024-03-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent_app', '0006_role_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
