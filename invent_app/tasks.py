# tasks.py (inside one of your Django apps)
from celery import shared_task
from datetime import datetime, timedelta
from .models import CustomUser
from django.core.mail import EmailMessage
from invent import settings
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

@shared_task
def send_email_after_delay(user_id):
    print(f"User Id: {user_id}")
    try:
        user = CustomUser.objects.get(pk=user_id)
        message = 'This is a confirmation that your background task has been executed.'
        emp_email = EmailMessage(
            "Testing",
            message,
            settings.EMAIL_HOST_USER,
            [user.email], 
        )   
        emp_email.send()
        print(f"Email sent to {user.email} at {datetime.now()}")
    except CustomUser.DoesNotExist:
        print("User does not exist.")


@shared_task
def backup_database():
    DB_NAME = os.getenv('DB_NAME', None)
    mysql_user = os.getenv('DB_USER', None)
    mysql_password = os.getenv('DB_PASSWORD', None)
    mysql_host = os.getenv('DB_HOST', None)
    mysql_port = os.getenv('DB_PORT', None)

    # Backup Configuration
    backup_dir = os.getenv('BACKUP_DIR', None)
    backup_zip_dir = os.getenv('BACKUP_ZIP_DIR',None)

    # Path to mysqldump and 7-Zip
    mysqldump_path = 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe'
    seven_zip_path = 'C:/Program Files/7-Zip/7z.exe'

    # Get current date and time
    current_datetime = datetime.now()
    backup_date = current_datetime.strftime('%Y-%m-%d')
    backup_time = current_datetime.strftime('%H-%M-%S')

    # Backup file name generation with full path
    backup_name = os.path.join(backup_dir, f'db_inventory_backup_{backup_date}_{backup_time}.sql')
    message = ""

    # Backup creation
    mysqldump_cmd = f'"{mysqldump_path}" --user={mysql_user} --password={mysql_password} --host={mysql_host} --port={mysql_port} {DB_NAME} > "{backup_name}"'
    if subprocess.call(mysqldump_cmd, shell=True) != 0:
        message = "Backup failed: error during dump creation"
        print('Backup failed: error during dump creation')
        return False

    # Backup compression
    backup_zip_name = f'{backup_zip_dir}/db_inventory_backup_{backup_date}_{backup_time}.zip'
    seven_zip_cmd = f'"{seven_zip_path}" a -tzip "{backup_zip_name}" "{backup_name}"'
    if subprocess.call(seven_zip_cmd, shell=True) != 0:
        message = 'Backup compression failed: error during archive creation'
        print('Backup compression failed: error during archive creation')
        return False
    message = f'Database backup success full for the hrms employee data: {backup_name}'
    # Delete temporary SQL file
    os.remove(backup_name)
    emp_email = EmailMessage(
            f'Database backup successfull:',
            message,
            settings.EMAIL_HOST_USER,
            ['amar.upadhyay@kasheemilk.com','kundan.chaurasia@kasheemilk.com','divyanshu.kumar@kasheemilk.com'], 
        )   
    emp_email.send()
    print('Backup successful')
    return True


@shared_task
def backup_only_data():
    DB_NAME = os.getenv('DB_NAME', None)
    mysql_user = os.getenv('DB_USER', '')
    mysql_password = os.getenv('DB_PASSWORD', '')
    mysql_host = os.getenv('DB_HOST', '')
    mysql_port = os.getenv('DB_PORT', '')
    # Backup Configuration
    backup_dir = os.getenv('DATA_BACKUP_DIR', '')
    backup_zip_dir = os.getenv('BACKUP_ZIP_DIR', '')

    # Path to mysqldump and 7-Zip
    mysqldump_path = 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe'
    seven_zip_path = 'C:/Program Files/7-Zip/7z.exe'

    # Get current date and time
    current_datetime = datetime.now()
    backup_date = current_datetime.strftime('%Y-%m-%d')
    backup_time = current_datetime.strftime('%H-%M-%S')
    message = ""
    # Backup file name generation with full path
    backup_name = os.path.join(backup_dir, f'db_inventory_backup_{backup_date}_{backup_time}.sql')

    # Backup creation
    mysqldump_cmd = f'"{mysqldump_path}" --user={mysql_user} --password={mysql_password} --host={mysql_host} --port={mysql_port} --no-create-info {DB_NAME} > "{backup_name}"'
    if subprocess.call(mysqldump_cmd, shell=True) != 0:
        message = "Backup failed: error during dump creation"
        print('Backup failed: error during dump creation')
        return False

    # Backup compression
    backup_zip_name = f'{backup_zip_dir}/db_inventory_backup_{backup_date}_{backup_time}.zip'
    seven_zip_cmd = f'"{seven_zip_path}" a -tzip "{backup_zip_name}" "{backup_name}"'
    if subprocess.call(seven_zip_cmd, shell=True) != 0:
        message = 'Backup compression failed: error during archive creation'
        print('Backup compression failed: error during archive creation')
        return False
    message = f'Database backup success full for the hrms employee data: {backup_name}'

    os.remove(backup_name)
    emp_email = EmailMessage(
            f'Database backup successfull:',
            message,
            settings.EMAIL_HOST_USER,
            ['amar.upadhyay@kasheemilk.com','kundan.chaurasia@kasheemilk.com','divyanshu.kumar@kasheemilk.com'], 
        )   
    emp_email.send()
    print('Backup successful')
    return True
