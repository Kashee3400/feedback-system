# Generated by Django 5.0 on 2024-05-11 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinary', '0004_remove_member_farmerid'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalbreed',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='animaldiagnosis',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='animaltreatment',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='animaltype',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='caseentry',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='casereceiverlog',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cattle',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cattlecasestatus',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cattlecasetype',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cattletagging',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='diagnosiscattlestatus',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='diagnosisroute',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='diagnosissymptoms',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='disease',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='doctormedicinestock',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicine',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicinecategory',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='medicinestock',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='onlinepayment',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='symptoms',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tagtype',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='sync',
            field=models.BooleanField(default=False),
        ),
    ]
