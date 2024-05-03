# Generated by Django 5.0 on 2024-05-03 05:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invent_app', '0015_awareness_awarenessimages_awarenessteammembers'),
    ]

    operations = [
        migrations.CreateModel(
            name='TAGType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_type', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'TAG Type',
                'verbose_name_plural': 'TAG Types',
                'db_table': 'tbl_tag_type',
            },
        ),
        migrations.AlterModelOptions(
            name='animalbreed',
            options={'verbose_name': 'Cattle Breed', 'verbose_name_plural': 'Cattle Breeds'},
        ),
        migrations.AlterModelOptions(
            name='animaltype',
            options={'verbose_name': 'Cattle Type', 'verbose_name_plural': 'Cattle Types'},
        ),
        migrations.RemoveField(
            model_name='disease',
            name='medicines',
        ),
        migrations.AddField(
            model_name='animals',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='disease',
            name='symptoms',
        ),
        migrations.CreateModel(
            name='CaseEntry',
            fields=[
                ('case_no', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_cases', to='invent_app.animals')),
                ('applied_by_ext', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_by_ext', to=settings.AUTH_USER_MODEL)),
                ('applied_by_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_cases', to='invent_app.member')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disease_cases', to='invent_app.disease')),
            ],
        ),
        migrations.AddField(
            model_name='animals',
            name='tag_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_animals', to='invent_app.tagtype'),
        ),
        migrations.AddField(
            model_name='disease',
            name='symptoms',
            field=models.ManyToManyField(related_name='symptom_disease', to='invent_app.symptoms'),
        ),
    ]
