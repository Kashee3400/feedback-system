# Generated by Django 5.0 on 2024-06-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent_app', '0007_employeerecentfeedbacklog_employeefeedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerecentfeedbacklog',
            name='recent_feedback',
            field=models.CharField(max_length=200),
        ),
    ]
