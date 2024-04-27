# Generated by Django 5.0 on 2024-04-20 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent_app', '0004_membercompaintreason_zerodayspourerreason'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membercompaintreason',
            options={'verbose_name': 'Member Complaint Reason', 'verbose_name_plural': 'Member Complaint Reasons'},
        ),
        migrations.AlterModelTable(
            name='membercompaintreason',
            table='tbl_member_complaint',
        ),
        migrations.CreateModel(
            name='MemberComplaintReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_member_complaints', to='invent_app.vcgmeeting')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='complaint_pouring', to='invent_app.member')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_complaint_reason', to='invent_app.membercompaintreason')),
            ],
            options={
                'verbose_name': 'Member Complaint Report',
                'verbose_name_plural': 'Member Complaint Reports',
                'db_table': 'tbl_member_complaint_report',
            },
        ),
        migrations.CreateModel(
            name='ZeroDaysPouringReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meeting_zero_days_pouring', to='invent_app.vcgmeeting')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='zerodays_pouring', to='invent_app.member')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zero_pouring_reason', to='invent_app.zerodayspourerreason')),
            ],
            options={
                'verbose_name': 'Zero Days Pouring Report',
                'verbose_name_plural': 'Zero Days Pouring Reports',
                'db_table': 'tbl_zerodays_report',
            },
        ),
    ]
