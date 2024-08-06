from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

#*****************************************************************************************************************#
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
    mcc = models.ForeignKey(VMCCs, on_delete=models.SET_NULL, null=True, related_name="facilitators")
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

import uuid

class VCGMeeting(models.Model):
    STARTED = 'started'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='meetings',verbose_name=_('User'))
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
        return f"{self.meeting_id}"

    def save(self, *args, **kwargs):
        if not self.meeting_id:
            unique_suffix = uuid.uuid4().hex[:6]  # Unique suffix for ensuring meeting_id is unique
            self.meeting_id = f"{self.mpp.mcc.mcc}_{self.mpp.mpp_loc}_{unique_suffix}"
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
    member = models.ForeignKey(VMembers, on_delete=models.CASCADE, related_name="zerodays_pouring")
    reason = models.ForeignKey(ZeroDaysPourerReason,  on_delete=models.CASCADE, related_name="zero_pouring_reason")
    meeting = models.ForeignKey(VCGMeeting, on_delete=models.CASCADE, related_name="meeting_zero_days_pouring")
        
    def __str__(self):
        return f'{self.member} - {self.reason}'
    
    class Meta:
        db_table = 'tbl_zerodays_report'
        verbose_name = 'Zero Days Pouring Report'
        verbose_name_plural = 'Zero Days Pouring Reports'

class MemberComplaintReport(models.Model):
    member = models.ForeignKey(VMembers, on_delete=models.CASCADE, related_name="complaint_pouring")
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
