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


from django.utils.timezone import now
import random
import string
from django.utils.translation import gettext_lazy as _ 

class EventSession(models.Model):
    session_name = models.CharField(
        max_length=255, 
        unique=True, 
        blank=True, 
        verbose_name=_('Session Name'),
        help_text=_('Unique name for the event session.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the session was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the session was last updated.')
    )

    def generate_session_name(self):
        # Get the current month and year
        current_month = now().strftime('%B')  # e.g., "September"
        current_year = now().strftime('%Y')   # e.g., "2024"

        # Generate a random 4-digit number to ensure uniqueness
        random_number = ''.join(random.choices(string.digits, k=4))

        # Create the session name
        return f"MPP Visit Report - {current_month} {current_year} - {random_number}"

    def save(self, *args, **kwargs):
        if not self.session_name:
            self.session_name = self.generate_session_name()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.session_name


class MppVisitBy(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name='mppvisit',
        help_text=_('Associated event session.')
    )
    facilitator_name = models.CharField(
        max_length=255, 
        verbose_name=_('Facilitator Name'),
        help_text=_('Name of the facilitator or Area Manager.')
    )
    mcc = models.CharField(
        max_length=255, 
        verbose_name=_('MCC'),
        help_text=_('MCC cname.')
    )
    mcc_code = models.CharField(
        max_length=50, 
        verbose_name=_('MCC Code'),
        help_text=_('MCC code.')
    )
    mpp = models.CharField(
        max_length=255, 
        verbose_name=_('MPP'),
        help_text=_('MPP code.')
    )
    mpp_name = models.CharField(
        max_length=255, 
        verbose_name=_('MPP Name'),
        help_text=_('Name of the MPP.')
    )
    no_of_pourer = models.IntegerField(
        verbose_name=_('Number of Pourer'),
        help_text=_('Number of pourers.')
    )
    no_of_non_member_pourer = models.IntegerField(
        blank=True, 
        null=True, 
        verbose_name=_('Number of Non-Member Pourers'),
        help_text=_('Number of pourers who are not members.')
    )
    sahayak_code = models.CharField(
        max_length=50, 
        blank=True,
        null=True,
        verbose_name=_('Sahayak Code'),
        help_text=_('In which code sahayak pouring non-member (Not a member of Kashee MPC) milk')
    )
    non_pourer_names = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Non-Pourer Names'),
        help_text=_('Names of non-pourers required, if "Number of Non-Member Pourers" more than 0.')
    )
    new_membership_enrolled = models.IntegerField(default=0,verbose_name=_('New Membership Enrolled'),help_text=_('How many new memberships are enrolled in kashee'))
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return self.facilitator_name


class CompositeData(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name="compositedata",
        help_text=_('Associated event session.')
    )
    qty = models.FloatField(
        verbose_name=_('Quantity'),
        help_text=_('Quantity of the composite data.')
    )
    fat = models.FloatField(
        verbose_name=_('Fat'),
        help_text=_('Fat content in the composite data.')
    )
    snf = models.FloatField(
        verbose_name=_('SNF'),
        help_text=_('SNF content in the composite data.')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return f"Qty: {self.qty}, Fat: {self.fat}, SNF: {self.snf}"


class DispatchData(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name="dispatchdata",
        help_text=_('Associated event session.')
    )
    qty = models.FloatField(
        verbose_name=_('Quantity'),
        help_text=_('Quantity of the dispatched data.')
    )
    fat = models.FloatField(
        verbose_name=_('Fat'),
        help_text=_('Fat content in the dispatched data.')
    )
    snf = models.FloatField(
        verbose_name=_('SNF'),
        help_text=_('SNF content in the dispatched data.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return f"Qty: {self.qty}, Fat: {self.fat}, SNF: {self.snf}"


class MaintenanceChecklist(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name="maintenancecheck",
        help_text=_('Associated event session.')
    )
    battery_water_level = models.BooleanField(
        default=False, 
        verbose_name=_('Battery Water Level'),
        help_text=_('Indicates if the battery water level is checked.')
    )
    weekly_cleaning_done = models.BooleanField(
        default=False, 
        verbose_name=_('Weekly Cleaning Done'),
        help_text=_('Indicates if weekly cleaning has been done.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return f"Battery Level Check: {self.battery_water_level},Weekly Cleaning Done: {self.weekly_cleaning_done}"


class ZeroPourerMembers(models.Model):
    mpp = models.CharField(
        max_length=200, 
        verbose_name=_('MPP'),
        help_text=_('MPP related to the member.')
    )
    name = models.CharField(
        max_length=200, 
        verbose_name=_('Name'),
        help_text=_('Name of the member.')
    )
    code = models.CharField(
        max_length=100, 
        verbose_name=_('Code'),
        help_text=_('Code associated with the member.')
    )
    updated_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the member record was last updated.')
    )
    created_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the member record was created.')
    )

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        db_table = 'tbl_zero_pourer_members'
        verbose_name = _('Zero Pourer Member')
        verbose_name_plural = _('Zero Pourer Members')


class NonPourerMeet(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name="nonpourermeet",
        help_text=_('Associated event session.')
    )
    member = models.ForeignKey(
        ZeroPourerMembers, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        verbose_name=_('Member'),
        help_text=_('Member who is a zero pourer.')
    )
    cow_in_milk = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_('Cows in Milk'),
        help_text=_('Number of cows in milk.')
    )
    cow_dry = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_('Dry Cows'),
        help_text=_('Number of dry cows.')
    )
    buff_in_milk = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_('Buffaloes in Milk'),
        help_text=_('Number of buffaloes in milk.')
    )
    buff_dry = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_('Dry Buffaloes'),
        help_text=_('Number of dry buffaloes.')
    )
    surplus = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_('Surplus'),
        help_text=_('Surplus amount.')
    )
    zero_days_reaason = models.ForeignKey(
        ZeroDaysPourerReason, 
        on_delete=models.SET_NULL,
        blank=True ,null=True,
        verbose_name=_('Zero Days Pouring Reason'),
        help_text=_('Zero days reason for not pouring milk.'))
    
    reason = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Reason'),
        help_text=_('Reason is required for other "zero_days_reaason" other.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    # def __str__(self):
    #     return str(self.member.name) if self.member else _('No Member')


class SessionVcgMeeting(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name="meetings",
        help_text=_('Associated event session.')
    )
    meeting_done = models.BooleanField(
        default=False, 
        verbose_name=_('Meeting Done'),
        help_text=_('Indicates if the VCG meeting was done.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return f"VCG Meeting Done: {self.meeting_done}"


class MembershipApp(models.Model):
    session = models.ForeignKey(
        EventSession, 
        on_delete=models.CASCADE, 
        verbose_name=_('Session'),
        related_name="membershipapp",
        help_text=_('Associated event session.')
    )
    no_of_installs = models.IntegerField(
        verbose_name=_('Number of Installs'),
        help_text=_('Number of installations.')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return f"Installs: {self.no_of_installs}"


class FormProgress(models.Model):
    STATUS_CHOICES = [
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    session = models.ForeignKey(EventSession, on_delete=models.CASCADE,related_name="formprogress")
    step = models.CharField(max_length=255)
    data = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-progress')
    timestamp = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session.session_name} - Step {self.step} ({self.status})"


class AgriculturalProducts(models.Model):
    session = models.ForeignKey(EventSession, on_delete=models.CASCADE,related_name="saledemands",blank=True,null=True)
    cf = models.IntegerField(
        verbose_name="CF", 
        help_text="Enter the value for CF", 
        default=0
    )
    mm = models.IntegerField(
        verbose_name="MM", 
        help_text="Enter the value for MM", 
        default=0
    )
    deverming = models.IntegerField(
        verbose_name="Deworming", 
        help_text="Enter the value for Deverming", 
        default=0
    )
    ss_utensils = models.IntegerField(
        verbose_name="SS Utensils", 
        help_text="Enter the value for SS Utensils", 
        default=0
    )
    fodder_seeds = models.IntegerField(
        verbose_name="Fodder Seeds", 
        help_text="Enter the value for Fodder Seeds", 
        default=0
    )
    created_at = models.DateTimeField(
        auto_now=True, 
        verbose_name=_('Created At'),
        help_text=_('Timestamp when the record was created.')
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True,null=True,
        verbose_name=_('Updated At'),
        help_text=_('Timestamp when the record was last updated.')
    )

    def __str__(self):
        return f"CF: {self.cf}, MM: {self.mm}, Deworming: {self.deverming}, Utensils: {self.ss_utensils}, Fodder Seeds: {self.fodder_seeds}"
