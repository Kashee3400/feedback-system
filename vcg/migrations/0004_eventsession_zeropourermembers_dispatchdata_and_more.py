# Generated by Django 5.0 on 2024-09-08 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcg', '0003_vcgmeeting_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_name', models.CharField(blank=True, help_text='Unique name for the event session.', max_length=255, unique=True, verbose_name='Session Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the session was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the session was last updated.', verbose_name='Updated At')),
            ],
        ),
        migrations.CreateModel(
            name='ZeroPourerMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpp', models.CharField(help_text='MPP related to the member.', max_length=200, verbose_name='MPP')),
                ('name', models.CharField(help_text='Name of the member.', max_length=200, verbose_name='Name')),
                ('code', models.CharField(help_text='Code associated with the member.', max_length=100, verbose_name='Code')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the member record was last updated.', verbose_name='Updated At')),
                ('created_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the member record was created.', verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Zero Pourer Member',
                'verbose_name_plural': 'Zero Pourer Members',
                'db_table': 'tbl_zero_pourer_members',
            },
        ),
        migrations.CreateModel(
            name='DispatchData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField(help_text='Quantity of the dispatched data.', verbose_name='Quantity')),
                ('fat', models.FloatField(help_text='Fat content in the dispatched data.', verbose_name='Fat')),
                ('snf', models.FloatField(help_text='SNF content in the dispatched data.', verbose_name='SNF')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
            ],
        ),
        migrations.CreateModel(
            name='CompositeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField(help_text='Quantity of the composite data.', verbose_name='Quantity')),
                ('fat', models.FloatField(help_text='Fat content in the composite data.', verbose_name='Fat')),
                ('snf', models.FloatField(help_text='SNF content in the composite data.', verbose_name='SNF')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
            ],
        ),
        migrations.CreateModel(
            name='FormProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(max_length=255)),
                ('data', models.JSONField()),
                ('status', models.CharField(choices=[('in-progress', 'In Progress'), ('completed', 'Completed')], default='in-progress', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceChecklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_water_level', models.BooleanField(default=False, help_text='Indicates if the battery water level is checked.', verbose_name='Battery Water Level')),
                ('weekly_cleaning_done', models.BooleanField(default=False, help_text='Indicates if weekly cleaning has been done.', verbose_name='Weekly Cleaning Done')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_installs', models.IntegerField(help_text='Number of installations.', verbose_name='Number of Installs')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
            ],
        ),
        migrations.CreateModel(
            name='MppVisitBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facilitator_name', models.CharField(help_text='Name of the facilitator.', max_length=255, verbose_name='Facilitator Name')),
                ('mcc', models.CharField(help_text='MCC code or name.', max_length=255, verbose_name='MCC')),
                ('mcc_code', models.CharField(help_text='MCC code.', max_length=50, verbose_name='MCC Code')),
                ('mpp', models.CharField(help_text='MPP code or name.', max_length=255, verbose_name='MPP')),
                ('mpp_name', models.CharField(help_text='Name of the MPP.', max_length=255, verbose_name='MPP Name')),
                ('no_of_pourer', models.IntegerField(help_text='Number of pourers.', verbose_name='Number of Pourer')),
                ('no_of_non_member_pourer', models.IntegerField(blank=True, help_text='Number of pourers who are not members.', null=True, verbose_name='Number of Non-Member Pourers')),
                ('sahayak_code', models.CharField(blank=True, help_text='Code for sahayak.', max_length=50, null=True, verbose_name='Sahayak Code')),
                ('non_pourer_names', models.TextField(blank=True, help_text='Names of non-pourers, if any.', null=True, verbose_name='Non-Pourer Names')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
            ],
        ),
        migrations.CreateModel(
            name='SessionVcgMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_done', models.BooleanField(default=False, help_text='Indicates if the VCG meeting was done.', verbose_name='Meeting Done')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
            ],
        ),
        migrations.CreateModel(
            name='NonPourerMeet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cow_in_milk', models.IntegerField(blank=True, default=0, help_text='Number of cows in milk.', null=True, verbose_name='Cows in Milk')),
                ('cow_dry', models.IntegerField(blank=True, default=0, help_text='Number of dry cows.', null=True, verbose_name='Dry Cows')),
                ('buff_in_milk', models.IntegerField(blank=True, default=0, help_text='Number of buffaloes in milk.', null=True, verbose_name='Buffaloes in Milk')),
                ('buff_dry', models.IntegerField(blank=True, default=0, help_text='Number of dry buffaloes.', null=True, verbose_name='Dry Buffaloes')),
                ('surplus', models.FloatField(blank=True, default=0, help_text='Surplus amount.', null=True, verbose_name='Surplus')),
                ('reason', models.TextField(blank=True, help_text='Reason for the surplus or other notes.', null=True, verbose_name='Reason')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created.', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated.', verbose_name='Updated At')),
                ('session', models.ForeignKey(help_text='Associated event session.', on_delete=django.db.models.deletion.CASCADE, to='vcg.eventsession', verbose_name='Session')),
                ('member', models.ForeignKey(blank=True, help_text='Member who is a zero pourer.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='vcg.zeropourermembers', verbose_name='Member')),
            ],
        ),
    ]
