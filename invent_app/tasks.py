# tasks.py (inside one of your Django apps)
from celery import shared_task
from datetime import datetime, timedelta
from .models import CustomUser,Feedback,FarmerFeedback
from django.core.mail import EmailMessage
from invent import settings
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()


def get_database_config():
    DB_NAME = os.getenv('DB_NAME')
    mysql_user = os.getenv('DB_USER', '')
    mysql_password = os.getenv('DB_PASSWORD', '')
    mysql_host = os.getenv('DB_HOST', '')
    mysql_port = os.getenv('DB_PORT', '')
    return DB_NAME, mysql_user, mysql_password, mysql_host, mysql_port

@shared_task
def backup_database():
    DB_NAME, mysql_user, mysql_password, mysql_host, mysql_port = get_database_config()
    backup_dir = os.getenv('BACKUP_DIR', "E:\MySQLBackups\DBBACKUP")
    mysqldump_path = 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe'
    seven_zip_path = 'C:/Program Files/7-Zip/7z.exe'

    backup_name = os.path.join(backup_dir, f'hrms_db_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql')
    mysqldump_cmd = f'"{mysqldump_path}" --user={mysql_user} --password={mysql_password} --host={mysql_host} --port={mysql_port} {DB_NAME} > "{backup_name}"'

    backup_zip_name = create_backup(DB_NAME, backup_dir, mysqldump_cmd, backup_name, 'Backup failed: error during dump creation',seven_zip_path)
    if backup_zip_name:
        message = f'Database backup success full for the hrms employee data: {backup_name}'        
        send_backup_email('Database backup successful:', message, ['divyanshu.kumar@kasheemilk.com'])
        print('DBMS Backup successful')
        return True
    return False

@shared_task
def backup_only_data():
    DB_NAME, mysql_user, mysql_password, mysql_host, mysql_port = get_database_config()
    backup_dir = os.getenv('DATA_BACKUP_DIR', '')
    mysqldump_path = 'C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe'
    seven_zip_path = 'C:/Program Files/7-Zip/7z.exe'

    backup_name = os.path.join(backup_dir, f'hrms_db_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql')
    mysqldump_cmd = f'"{mysqldump_path}" --user={mysql_user} --password={mysql_password} --host={mysql_host} --port={mysql_port} --no-create-info {DB_NAME} > "{backup_name}"'

    backup_zip_name = create_backup(DB_NAME, backup_dir, mysqldump_cmd, backup_name, 'Backup failed: error during dump creation',seven_zip_path)
    if backup_zip_name:
        message = f'Database backup success full for the hrms employee data: {backup_name}'
        send_backup_email('Database backup successful:', message, ['divyanshu.kumar@kasheemilk.com'])
        print('Data Backup successful')
        return True
    return False


def send_backup_email(subject, message, recipients):
    emp_email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipients)
    emp_email.send()

def create_backup(DB_NAME, backup_dir, mysqldump_cmd, backup_name, message,seven_zip_path):
    if subprocess.call(mysqldump_cmd, shell=True) != 0:
        print(message)
        return False
    backup_zip_name = f'{backup_dir}/{DB_NAME}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.zip'
    seven_zip_cmd = f'"{seven_zip_path}" a -tzip "{backup_zip_name}" "{backup_name}"'
    if subprocess.call(seven_zip_cmd, shell=True) != 0:
        print('Backup compression failed: error during archive creation')
        return False
    os.remove(backup_name)
    return backup_zip_name



@shared_task
def auto_forward_feedbacks():
    pass