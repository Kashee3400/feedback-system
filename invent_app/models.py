from django.contrib.auth.models import AbstractUser
from django.db import models
from channels.layers import get_channel_layer
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta
from django.utils import timezone
import uuid


from enum import Enum

class RoleCode(Enum):
    SAHAYAK = 'sahayak'
    GRO = 'gro'
    HOD = 'hod'
    MEMBER = 'member'
    USER = 'user'
    CE = 'ce'


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department
    
    class Meta:
        db_table = 'tbl_department'
        managed = True
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Logo(models.Model):
    image = models.ImageField(upload_to='images/')

    class Meta:
        db_table = 'educart_logo'
        managed = True
        verbose_name = 'Logo'
        verbose_name_plural = 'Logoes'


class Role(models.Model):
    role = models.CharField(max_length=20, blank=True, null=True)
    role_code = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in RoleCode], primary_key=True)

    def __str__(self):
        return self.role

    class Meta:
        db_table = 'tbl_role'
        managed = True
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,blank=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,blank=True,null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    
    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username
    
    class Meta:
        db_table = 'tbl_user'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_confirmation'
        managed = True
        verbose_name = 'Email Confirmation'
        verbose_name_plural = 'Email Confirmations'


class OTPToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(blank=True,null=True)

    class Meta:
        db_table = 'otp_token'
        managed = True
        verbose_name = 'OTP Token'
        verbose_name_plural = 'OTP Tokens'

    def __str__(self):
        return self.token
    
class Designation(models.Model):
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.designation
    
    class Meta:
        db_table = 'tbl_designation'
        managed = True
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='user_profile')
    desination = models.ForeignKey(Designation, on_delete=models.CASCADE,null=True, blank=True)
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, default=0)
    gender = models.CharField(max_length=200,choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        today = datetime.today()
        dob = self.dob
        if dob:
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            self.age = age
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} {self.dob}"
    
    def update_user_data(self, first_name, last_name, email):
        self.user.first_name = first_name
        self.user.last_name = last_name
        self.user.email = email
        self.user.save()
        
class Location(models.Model):
    mcc = models.CharField(max_length = 100)
    mcc_code = models.CharField(max_length = 20,primary_key=True,default = "EX_CODE")
    
    def __str__(self):
        return f"{self.mcc}"
    
    class Meta:
        db_table = 'tbl_location'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
class SubLocations(models.Model):
    mcc = models.ForeignKey(Location, on_delete = models.CASCADE)
    mpp_loc = models.CharField(max_length = 100)
    mpp_loc_code = models.CharField(max_length = 20,primary_key=True,default = "EX_CODE")
    
    def __str__(self):
        return f"MPP CODE ({self.mpp_loc_code}), MPP ({self.mpp_loc})"
    
    class Meta:
        db_table = 'tbl_sub_location'
        verbose_name = 'Sub Location'
        verbose_name_plural = 'Sub Locations'


class FeedbackCategory(models.Model):
    category = models.CharField(max_length=50)
    days = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category}"
    
    class Meta:
        db_table = 'tbl_feedback_categories'
        verbose_name = 'Feedback Category'
        verbose_name_plural = 'Feedback Categories'



import uuid
from django.db import models
from django.utils import timezone

class BaseFeedback(models.Model):
    # Fields related to feedback
    mcc_code = models.CharField(max_length=5, blank=True, null=True)
    mcc_ex_code = models.CharField(max_length=20, blank=True, null=True)
    mcc_name = models.CharField(max_length=255, blank=True, null=True)
    mpp_code = models.CharField(max_length=9, blank=True, null=True)
    mpp_ex_code = models.CharField(max_length=20, blank=True, null=True)
    mpp_short_name = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True)
    re_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    reopened_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    feedback_id = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    remark = models.TextField(blank=True, editable=False)
    message = models.TextField()

    def close_feedback(self):
        self.is_closed = True
        self.resolved_at = timezone.now()

    def reopen_feedback(self):
        self.is_closed = False
        self.reopened_at = timezone.now()

    def save(self, *args, **kwargs):
        if not self.feedback_id:
            self.feedback_id = 'Feed' + str(uuid.uuid4().hex)[:6]  # Generate random text
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class FarmerFeedback(BaseFeedback):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_farmer_feedbacks', blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    receiver_farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='farmer_feedbacks_received')
    mpp = models.ForeignKey(SubLocations, on_delete=models.CASCADE, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.sender:
            return f"Feedback from {self.sender.username}"
        else:
            return f"Feedback from {self.name}"

    def forward_to_hod(self, role, department=None):
        hod = CustomUser.objects.filter(role=role, department=department).first() if department else CustomUser.objects.filter(is_superuser=True).first()
        if hod:
            self.receiver_farmer = hod

class FarmerFeedbackFile(models.Model):
    feedback = models.ForeignKey(FarmerFeedback, on_delete=models.CASCADE, related_name='farmer_files')
    file = models.FileField(upload_to='feedback_files/')

class Feedback(BaseFeedback):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_feedbacks')
    receiver_feedback = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='feedbacks_received')
    sub_location = models.ForeignKey(SubLocations, on_delete=models.CASCADE, blank=True, null=True)
    feedback_cat = models.ForeignKey(FeedbackCategory, on_delete=models.CASCADE, blank=True, null=True)

    def forward_to_hod(self, role, department=None):
        hod = CustomUser.objects.filter(role=role, department=department).first() if department else CustomUser.objects.filter(is_superuser=True).first()
        if hod:
            self.receiver_feedback = hod

    def __str__(self):
        return f"Feedback from {self.sender.username} - {self.message}"


class LanguageSopported(models.Model):
    title = models.CharField(max_length=30)
    code = models.CharField(max_length = 100,primary_key=True, default="en-US")
    img = models.ImageField(upload_to='language_icons', blank=True,null=True)
    
    def __str__(self):
        return f"({self.title}) - ({self.code})"
    
    class Meta:
        db_table = 'tbl_lang_supported'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'


# @receiver(post_save, sender=CustomUser)
# def user_change_handler(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "users_group", 
#         {
#             "type": "user_change",
#             "user_id": instance.id,
#         }
#     )


# @receiver(post_save, sender=CustomUser)
# def user_created_handler(sender, instance, created, **kwargs):
#     if created:
#         print(instance.username)
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "users_group", 
#             {
#                 "type": "user_change",
#                 "user_id": instance.id,
#             }
#         )

# @receiver(post_delete, sender=CustomUser)
# def user_delete_handler(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     print(instance.username)
#     async_to_sync(channel_layer.group_send)(
#         "users_group", 
#         {
#             "type": "user_delete",
#             "user_id": instance.id,
#         }
#     )
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    
class MCCs(models.Model):
    mcc = models.CharField(max_length = 100)
    mcc_code = models.CharField(max_length = 20,primary_key=True,default = "EX_CODE")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.mcc}"
    
    class Meta:
        db_table = 'tbl_mcc'
        verbose_name = 'MCC'
        verbose_name_plural = 'MCCs'
    

class MPPs(models.Model):
    mcc = models.ForeignKey(MCCs, on_delete = models.CASCADE, related_name="mpps")
    mpp_loc = models.CharField(max_length = 100)
    mpp_loc_code = models.CharField(max_length = 20,primary_key=True,default = "EX_CODE")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.mpp_loc}-({self.mpp_loc_code})"
    
    class Meta:
        db_table = 'tbl_mpp'
        verbose_name = 'MPP'
        verbose_name_plural = 'MPPs'

class EmployeeRecentFeedbackLog(models.Model):
    recent_feedback = models.CharField(max_length=200)
    
    def __str__(self):
        return self.recent_feedback
    
    class Meta:
        db_table = 'tbl_employee_feedback'
        verbose_name = 'Employee Recent FeedbackLog'
        verbose_name_plural = 'Employee Recent FeedbackLogs'
    
class EmployeeFeedback(models.Model):
    CLOSED,OPENED, OK =  'Closed','Open', 'OK'
    status_choices = [
        (OPENED, 'Open'),
        (CLOSED, 'Closed'),
        (OK, 'Ok'),
    ]
    sender = models.ForeignKey(CustomUser, related_name='emp_sent_feedbacks', on_delete=models.CASCADE)
    receivers = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True, related_name='emp_received_feedbacks')
    forwarded_to = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True, related_name='emp_forwarded_feedbacks', blank=True)
    status = models.CharField(max_length=10, choices=status_choices, default=OPENED)
    feedback = models.CharField(max_length=200,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    re_message = models.TextField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    reopened_at = models.DateTimeField(null=True, blank=True)
    feedback_id = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    
    def reopen(self):
        if self.status == self.CLOSED:
            self.status = self.OPENED
            self.save()

    def close_feedback(self):
        if self.status == self.OPENED:
            self.status = self.CLOSED
            self.save()
            
    def ok_feedback(self):
        self.status = self.OK
        self.save()

    def forward_to(self, user):
        if user != self.sender and user not in self.receivers.all():
            self.forwarded_to.add(user)
            self.save()

    def __str__(self):
        return f"Feedback from {self.sender} to {', '.join(str(user) for user in self.receivers.all())} ({self.status})"
    
    def save(self, *args, **kwargs):
        if not self.feedback_id:
            self.feedback_id = 'Feed' + str(uuid.uuid4().hex)[:6] 
        super().save(*args, **kwargs)


