# Generated by Django 5.0 on 2024-04-02 06:59

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Designation',
                'verbose_name_plural': 'Designations',
                'db_table': 'tbl_designation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('mcc', models.CharField(max_length=100)),
                ('mcc_code', models.CharField(default='EX_CODE', max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'db_table': 'tbl_location',
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
            ],
            options={
                'verbose_name': 'Logo',
                'verbose_name_plural': 'Logoes',
                'db_table': 'educart_logo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role', models.CharField(blank=True, max_length=20, null=True)),
                ('role_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.department')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.role')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EmailConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email Confirmation',
                'verbose_name_plural': 'Email Confirmations',
                'db_table': 'email_confirmation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FeedbackCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('days', models.IntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_category', to='invent_app.department')),
            ],
            options={
                'verbose_name': 'Feedback Category',
                'verbose_name_plural': 'Feedback Categories',
                'db_table': 'tbl_feedback_categories',
            },
        ),
        migrations.CreateModel(
            name='OTPToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiry_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OTP Token',
                'verbose_name_plural': 'OTP Tokens',
                'db_table': 'otp_token',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('age', models.IntegerField(default=0, null=True)),
                ('gender', models.CharField(blank=True, default='NA', max_length=200, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('desination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.designation')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'db_table': 'user_profile',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SubLocations',
            fields=[
                ('mpp_loc', models.CharField(max_length=100)),
                ('mpp_loc_code', models.CharField(default='EX_CODE', max_length=20, primary_key=True, serialize=False)),
                ('mcc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invent_app.location')),
            ],
            options={
                'verbose_name': 'Sub Location',
                'verbose_name_plural': 'Sub Locations',
                'db_table': 'tbl_sub_location',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('mobile', models.CharField(blank=True, max_length=50, unique=True)),
                ('re_message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('reopened_at', models.DateTimeField(blank=True, null=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('feedback_id', models.CharField(blank=True, editable=False, max_length=50, unique=True)),
                ('remark', models.TextField(blank=True, editable=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='feedback_files/')),
                ('receiver_feedback', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_feedbacks', to=settings.AUTH_USER_MODEL)),
                ('feedback_cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.feedbackcategory')),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.priority')),
                ('sub_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.sublocations')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FarmerFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('mobile', models.CharField(blank=True, max_length=50, unique=True)),
                ('re_message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('reopened_at', models.DateTimeField(blank=True, null=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('feedback_id', models.CharField(blank=True, editable=False, max_length=50, unique=True)),
                ('remark', models.TextField(blank=True, editable=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='feedback_files/')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('receiver_farmer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_feedbacks_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_farmer_feedbacks', to=settings.AUTH_USER_MODEL)),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.priority')),
                ('mpp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invent_app.sublocations')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
