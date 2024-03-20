from django.contrib.auth.models import AbstractUser
from django.db import models
from channels.layers import get_channel_layer
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from datetime import datetime, timedelta


class Logo(models.Model):
    image = models.ImageField(upload_to='images/')

    class Meta:
        db_table = 'educart_logo'
        managed = True
        verbose_name = 'Logo'
        verbose_name_plural = 'Logoes'



from django.contrib.auth.models import AbstractUser

from django.db import models

class Role(models.Model):
    role = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return self.role


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,blank=True,null=True)

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


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    age = models.IntegerField(null=True, default=0)
    gender = models.CharField(max_length=200, default="NA", null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        today = datetime.today()
        dob = self.dob
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        self.age = age
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} {self.dob}"


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department
    
class FeedbackCategory(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_category')
    category = models.CharField(max_length=50)
    def __str__(self):
        return f"Feedback Category {self.department.department} {self.category}"

class Feedback(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_feedbacks')
    feedback_cat = models.ForeignKey(FeedbackCategory, on_delete=models.CASCADE,blank=True,null=True)
    district = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    def forward_to_hod(self):
        hod = CustomUser.objects.filter(role=CustomUser.HOD, department=self.department).first()
        if hod:
            self.receiver = hod
        else:
            # If no HOD found, forward to admin
            self.receiver = CustomUser.objects.filter(role=CustomUser.ADMIN).first()

    def close_feedback(self):
        self.is_closed = True
        self.resolved_at = datetime.now()

    def __str__(self):
        return f"Feedback from {self.sender.username} in {self.department.name} department - {self.subject}"


@receiver(post_save, sender=CustomUser)
def user_change_handler(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "users_group", 
        {
            "type": "user_change",
            "user_id": instance.id,
        }
    )


@receiver(post_save, sender=CustomUser)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        print(instance.username)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "users_group", 
            {
                "type": "user_change",
                "user_id": instance.id,
            }
        )

@receiver(post_delete, sender=CustomUser)
def user_delete_handler(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    print(instance.username)
    async_to_sync(channel_layer.group_send)(
        "users_group", 
        {
            "type": "user_delete",
            "user_id": instance.id,
        }
    )
    