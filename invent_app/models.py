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
    CE = 'ce'


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department

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


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,blank=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username


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
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
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
    
class FeedbackCategory(models.Model):
    category = models.CharField(max_length=50)
    days = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category}"
    
    class Meta:
        db_table = 'tbl_feedback_categories'
        verbose_name = 'Feedback Category'
        verbose_name_plural = 'Feedback Categories'


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

class BaseFeedback(models.Model):
    message = models.TextField()
    mobile = models.CharField(max_length=50, blank=True)
    re_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    reopened_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    feedback_id = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    remark =  models.TextField(blank=True, editable=False)
    file = models.FileField(upload_to='feedback_files/', null=True, blank=True)


    def close_feedback(self):
        self.is_closed = True
        self.resolved_at = timezone.now()

    def reopen_feedback(self):
        self.is_closed = False
        self.reopened_at = timezone.now()

        
    def save(self, *args, **kwargs):
        # Generate a random feedback ID starting with "Feed"
        if not self.feedback_id:
            self.feedback_id = 'Feed' + str(uuid.uuid4().hex)[:6]  # Generate random text
        
        super().save(*args, **kwargs)
        
    class Meta:
        abstract = True

class FarmerFeedback(BaseFeedback):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_farmer_feedbacks',blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    receiver_farmer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='farmer_feedbacks_received')
    mpp = models.ForeignKey(SubLocations, on_delete=models.CASCADE, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.sender:
            return f"Feedback from {self.sender.username} "
        else:
            return f"Feedback from {self.name} "

    def forward_to_hod(self, role, department=None):
        hod = CustomUser.objects.filter(role=role, department=department).first() if department else CustomUser.objects.filter(is_superuser=True).first()
        if hod:
            self.receiver_farmer = hod

class Feedback(BaseFeedback):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_feedbacks')
    receiver_feedback = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='feedbacks_received')
    sub_location = models.ForeignKey(SubLocations, on_delete=models.CASCADE, blank=True, null=True)
    feedback_cat = models.ForeignKey(FeedbackCategory, on_delete=models.CASCADE, blank=True, null=True)

    def forward_to_hod(self, role, department=None):
        hod = CustomUser.objects.filter(role=role, department=department).first() if department else CustomUser.objects.filter(is_superuser=True).first()
        print(hod)
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

class Member(models.Model):
    FarmerId =  models.IntegerField(blank=True, null=True)
    FarmerCode = models.CharField(max_length=100, unique=True,primary_key=True)
    FullName = models.CharField(max_length=255)
    FatherName = models.CharField(max_length=255, blank=True,null=True)
    EmailAddress = models.EmailField(blank=True,null=True)
    PhoneNumber = models.CharField(max_length=20,null=True)
    PlantID = models.IntegerField(blank=True, null=True)
    PlantCode = models.CharField(max_length=20, blank=True,null=True)
    PlantName = models.CharField(max_length=100)
    MccID = models.IntegerField(blank=True, null=True)
    MccCode = models.CharField(max_length=20, blank=True,null=True)
    MccName = models.CharField(max_length=100)
    MstCenterCode = models.IntegerField()
    BmcName = models.CharField(max_length=100)
    SocietyCode = models.IntegerField(blank=True, null=True)
    SocietyName = models.CharField(max_length=100)
    CompanyId = models.IntegerField(blank=True, null=True)
    AddressLine1 = models.CharField(max_length=255, blank=True,null=True)
    AddressLine2 = models.CharField(max_length=255, blank=True,null=True)
    City = models.CharField(max_length=100, blank=True,null=True)
    Pincode = models.CharField(max_length=20, blank=True,null=True)
    VillageId = models.IntegerField(blank=True, null=True)
    DistrictId = models.IntegerField(blank=True, null=True)
    DistrictName = models.CharField(max_length=100)
    StateId = models.IntegerField(blank=True, null=True)
    StateName = models.CharField(max_length=100)
    VillageName = models.CharField(max_length=100)
    IsRegistered = models.BooleanField(default=False)
    RegistrationDate = models.DateTimeField(blank=True, null=True)
    OTP = models.CharField(max_length=255, blank=True,null=True)
    EncToken = models.TextField(blank=True,null=True)
    DefaultLanguage = models.IntegerField(blank=True, null=True)
    otpsms = models.TextField(blank=True, null=True)
    opt_status = models.CharField(max_length=255, blank=True, null=True)
    smsurl = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.FarmerCode

    class Meta:
        db_table = 'tbl_members'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

class AnimalType(models.Model):
    animal_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.animal_type
    
    class Meta:
        db_table = 'tbl_animal_type'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'


class AnimalBreed(models.Model):
    breed = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name='breeds')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.breed}"
    
    class Meta:
        db_table = 'tbl_animal_breed'
        verbose_name = 'Animal Breed'
        verbose_name_plural = 'Animal Breeds'


class Animals(models.Model):
    farmer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="farmer_animals")
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE, related_name='breed_animals')
    tag_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.breed.animal_type} - {self.breed} - {self.tag_number}"

    class Meta:
        db_table = 'tbl_animals'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'


class Symptoms(models.Model):
    symptom = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbl_animal_symptoms'
        verbose_name = 'Symptom'
        verbose_name_plural = 'Symptoms'


class Medicine(models.Model):
    medicine = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.medicine

    class Meta:
        db_table = 'tbl_medicines'
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'


class Disease(models.Model):
    disease = models.CharField(max_length=100)
    symptoms = models.TextField()
    medicines = models.ManyToManyField(Medicine)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.disease
    
    class Meta:
        db_table = 'tbl_disease'
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'


class AnimalTreatment(models.Model):
    animal = models.ForeignKey(Animals, on_delete=models.CASCADE, related_name="animal_treatment")
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name="disease_treatment")
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="treatments_done")
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField()

    def __str__(self):
        return f"{self.animal} - {self.disease} - {self.date}"

    class Meta:
        db_table = 'tbl_animal_treatments'
        verbose_name = 'AnimalTreatment'
        verbose_name_plural = 'AnimalTreatments'



# VCG Meeting tables

class VMCCs(models.Model):
    mcc = models.CharField(max_length = 100)
    mcc_code = models.CharField(max_length = 20,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.mcc}"
    
    class Meta:
        db_table = 'tbl_vcg_mcc'
        verbose_name = 'VCG MCC'
        verbose_name_plural = 'VCG MCCs'
    

class VMPPs(models.Model):
    mcc = models.ForeignKey(VMCCs, on_delete = models.CASCADE, related_name="mcc_mpps_list")
    mpp_loc = models.CharField(max_length = 100)
    mpp_loc_code = models.CharField(max_length = 20,primary_key=True)
    district = models.CharField(max_length = 20,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.mpp_loc}-({self.mpp_loc_code})"
    
    class Meta:
        db_table = 'tbl_vcg_mpp'
        verbose_name = 'VCG MPP'
        verbose_name_plural = 'VCG MPPs'
        

class Facilitator(models.Model):
    mcc = models.ForeignKey(VMCCs, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.mcc} - {self.name}"
    
    class Meta:
        db_table = 'tbl_facilitators'
        verbose_name = 'Facilitator'
        verbose_name_plural = 'Facilitators'


class VMembers(models.Model):
    mpp = models.ForeignKey(VMPPs, on_delete=models.SET_NULL, null=True,related_name="mpp_members")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length = 100)
    max_qty = models.FloatField(default=0)
    cattle_bag = models.IntegerField(default=0)
    mineral_bag = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        db_table = 'tbl_vmembers'
        verbose_name = 'V Member'
        verbose_name_plural = 'V Members'


class VCGroup(models.Model):
    whatsapp_num = models.CharField(max_length=20,blank=True,null=True)
    member = models.ForeignKey(VMembers, on_delete=models.CASCADE, related_name="member_group")

    def __str__(self):
        return f"{self.member} ({self.whatsapp_num})"

    class Meta:
        db_table = 'tbl_vcg_member'
        verbose_name = 'VCG Group'
        verbose_name_plural = 'VCG Groups'

class ConductedByType(models.Model):
    conducted_type =  models.CharField(max_length=50)
    created_dat = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return f"{self.conducted_type}"


    class Meta:
        db_table = 'tbl_conducted_type'
        verbose_name = 'Conducted By Type'
        verbose_name_plural = 'Conducted By Types'


class ConductedByName(models.Model):
    type =  models.ForeignKey(ConductedByType,on_delete=models.CASCADE,related_name="conducted_by_type")
    name =  models.CharField(max_length=50)
    created_dat = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        db_table = 'tbl_conducted_name'
        verbose_name = 'Conducted By Name'
        verbose_name_plural = 'Conducted By Names'


class VCGMeeting(models.Model):
    STARTED = 'started'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
    )
    mpp = models.ForeignKey(VMPPs, on_delete=models.CASCADE, related_name="mpp_vcg_meetings")
    conducted_by_type = models.ForeignKey(ConductedByType, on_delete=models.CASCADE, related_name="vcg_meeting_conducted_type",blank=True, null=True)
    conducted_by_name = models.ForeignKey(ConductedByName, on_delete=models.CASCADE, related_name="vcg_meeting_conducted_name",blank=True, null=True)
    conducted_by_fs = models.ForeignKey(Facilitator, on_delete=models.CASCADE, related_name="vcg_meeting_conducted_fs",blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    meeting_id = models.CharField(max_length=100, unique=True, default="")
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STARTED)    

    def __str__(self):
        return f"{self.mpp} - {self.meeting_id} ({self.conducted_by_type})"

    def save(self, *args, **kwargs):
        self.meeting_id = f"{self.mpp.mcc.mcc_code}_{self.mpp.mpp_loc_code}_{self.start_datetime}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'tbl_vcg_meeting'
        verbose_name = 'VCG Meeting'
        verbose_name_plural = 'VCG Meetings'

class VCGMemberAttendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]
    meeting = models.ForeignKey(VCGMeeting, on_delete=models.CASCADE, related_name="attendances",blank=True, null=True)
    member = models.ForeignKey(VCGroup, on_delete=models.CASCADE, related_name="vcg_attendance",blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default=ABSENT)
    date = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.member} ({self.status})"


    class Meta:
        db_table = 'tbl_member_attendance'
        verbose_name = 'VCG Member Attendance'
        verbose_name_plural = 'VCG Member Attendances'

class VCGMeetingImages(models.Model):
    meeting = models.ForeignKey(VCGMeeting, on_delete=models.CASCADE, related_name="meeting_images",blank=True, null=True)
    image = models.FileField(upload_to="meeting_images")
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.meeting}"

    class Meta:
        db_table = 'tbl_meeting_images'
        verbose_name = 'VCG Meeting Images'
        verbose_name_plural = 'VCG Meeting Images'


class ZeroDaysPourerReason(models.Model):
    reason = models.CharField(max_length=150)
    
    def __str__(self):
        return self.reason
    
    class Meta:
        db_table = 'tbl_zero_days_pouring'
        verbose_name = 'Zero days pouring Reason'
        verbose_name_plural = 'Zero days pouring Reasons'

class MemberCompaintReason(models.Model):
    reason = models.CharField(max_length=150)
    
    def __str__(self):
        return self.reason
    
    class Meta:
        db_table = 'tbl_member_complaint'
        verbose_name = 'Member Complaint Reason'
        verbose_name_plural = 'Member Complaint Reasons'

    
class ZeroDaysPouringReport(models.Model):
    member = models.OneToOneField(VMembers, on_delete=models.CASCADE, related_name="zerodays_pouring")
    reason = models.ForeignKey(ZeroDaysPourerReason,  on_delete=models.CASCADE, related_name="zero_pouring_reason")
    meeting = models.ForeignKey(VCGMeeting, on_delete=models.CASCADE, related_name="meeting_zero_days_pouring")
        
    def __str__(self):
        return f'{self.member} - {self.reason}'
    
    class Meta:
        db_table = 'tbl_zerodays_report'
        verbose_name = 'Zero Days Pouring Report'
        verbose_name_plural = 'Zero Days Pouring Reports'

class MemberComplaintReport(models.Model):
    member = models.OneToOneField(VMembers, on_delete=models.CASCADE, related_name="complaint_pouring")
    reason = models.ForeignKey(MemberCompaintReason,  on_delete=models.CASCADE, related_name="member_complaint_reason")
    meeting = models.ForeignKey(VCGMeeting, on_delete=models.CASCADE, related_name="meeting_member_complaints")
    
    
    def __str__(self):
        return f'{self.member} - {self.reason}'
    
    class Meta:
        db_table = 'tbl_member_complaint_report'
        verbose_name = 'Member Complaint Report'
        verbose_name_plural = 'Member Complaint Reports'

class MonthAssignment(models.Model):
    mpp = models.OneToOneField(VMPPs, on_delete=models.CASCADE, related_name='mpp_assignment')
    milk_collection = models.FloatField(default=0, help_text='Milk Collection (Liters/Day)')
    no_of_members = models.IntegerField(default=0, help_text='No of Members')
    no_of_pourers = models.IntegerField(default=0, help_text='No Of Pourers')
    pourers_15_days = models.IntegerField(default=0, help_text='>=15 Days Pourers')
    pourers_25_days = models.IntegerField(default=0, help_text='>=25 Days Pourers')
    zero_days_pourers = models.IntegerField(default=0, help_text='Zero Days Pourers')
    cattle_feed_sale = models.FloatField(default=0, help_text='Cattle Feed Sale (KG)')
    mineral_mixture_sale = models.FloatField(default=0, help_text='Mineral Mixture Sale (KG)')
    sahayak_recovery = models.FloatField(default=0, help_text='Sahayak Recovery (%)')

    def __str__(self):
        return f'Month Assignment #{self.pk} {self.mpp.mpp_loc}'

    class Meta:
        db_table = 'tbl_month_assignment'
        verbose_name = 'Month Assignment'
        verbose_name_plural = 'Month Assignments'

class Awareness(models.Model):
    mpp = models.OneToOneField(VMPPs, on_delete=models.CASCADE, related_name='mpp_awareness')
    no_of_participants = models.IntegerField(default=0, help_text='No of Members')
    leader_name = models.CharField(max_length=100, help_text='Team Leader Name')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Awareness #{self.pk} {self.leader_name}'

    class Meta:
        db_table = 'tbl_awareness'
        verbose_name = 'Awareness'
        verbose_name_plural = 'Awarenesses'


class AwarenessImages(models.Model):
    awareness = models.ForeignKey(Awareness, on_delete=models.CASCADE, related_name="awareness_images",blank=True, null=True)
    image = models.FileField(upload_to="awareness_images")
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.awareness}"

    class Meta:
        db_table = 'tbl_awareness_images'
        verbose_name = 'Awareness Images'
        verbose_name_plural = 'Awareness Images'


class AwarenessTeamMembers(models.Model):
    awareness = models.ForeignKey(Awareness, on_delete=models.CASCADE, related_name="awareness_team",blank=True, null=True)
    member_name = models.CharField(max_length=100, help_text='Team Member Name')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Team Member #{self.pk} {self.member_name}'

    class Meta:
        db_table = 'tbl_awareness_team_member'
        verbose_name = 'Awareness Team Member'
        verbose_name_plural = 'Awareness Team Members'

