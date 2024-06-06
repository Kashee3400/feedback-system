from django.db import models
from invent_app.models import CustomUser
from vcg.models import VMCCs,VMPPs
from datetime import timezone

# ************************  Veterinary Tables ********************************* #

class Member(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.SET_NULL,blank=True,null=True)
    FarmerCode = models.CharField(max_length=100, unique=True,primary_key=True)
    FatherName = models.CharField(max_length=255, blank=True,null=True)
    mpp = models.ForeignKey(VMPPs,blank=True, null=True,on_delete=models.SET_NULL)
    VillageId = models.IntegerField(blank=True, null=True)
    DistrictId = models.IntegerField(blank=True, null=True)
    DistrictName = models.CharField(max_length=100)
    StateId = models.IntegerField(blank=True, null=True)
    StateName = models.CharField(max_length=100)
    VillageName = models.CharField(max_length=100)
    IsRegistered = models.BooleanField(default=False)
    RegistrationDate = models.DateTimeField(blank=True, null=True)
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
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return self.animal_type
    
    class Meta:
        db_table = 'tbl_animal_type'
        verbose_name = 'Cattle Type'
        verbose_name_plural = 'Cattle Types'

class BankAccount(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="bank_account")
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    bank_short_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    IFSC_code = models.CharField(max_length=20)
    sync = models.BooleanField(default=False)

    def __str__(self):
        return f"Bank Account for {self.user.username}"

    class Meta:
        db_table = 'tbl_user_bank_account'
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'


class AnimalBreed(models.Model):
    breed = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name='breeds')
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.breed}"
    
    class Meta:
        db_table = 'tbl_animal_breed'
        verbose_name = 'Cattle Breed'
        verbose_name_plural = 'Cattle Breeds'

class TAGType(models.Model):
    tag_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.tag_type}"
    
    class Meta:
        db_table = 'tbl_tag_type'
        verbose_name = 'TAG Type'
        verbose_name_plural = 'TAG Types'


class Cattle(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    farmer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="farmer_animals")
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE, related_name='breed_animals')
    tag_type = models.ForeignKey(TAGType, on_delete=models.CASCADE, related_name='tag_animals', null=True, blank=True)
    tag_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.PositiveBigIntegerField(null=True, blank=True)
    sync = models.BooleanField(default=False)
 

    def __str__(self):
        return f"{self.breed.animal_type} - {self.breed} - {self.tag_number}"

    class Meta:
        db_table = 'tbl_animals'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'

    @property
    def cases(self):
        return self.cattle_cases.all()

    @property
    def treatments(self):
        return AnimalTreatment.objects.filter(case_treatment__animal=self)

    def all_details(self):
        animal_details = {
            "animal": self,
            "cases": list(self.cases),
            "treatments": list(self.treatments)
        }
        return animal_details
    
    class Meta:
        db_table = 'tbl_cattle'
        verbose_name = 'Cattle'
        verbose_name_plural = 'Cattles'



class CattleTagging(models.Model):
    cattle = models.OneToOneField(Cattle, on_delete=models.CASCADE, related_name="cattle_tagged")
    tag_number = models.CharField(max_length=20)
    tagging_date = models.DateField(auto_now=True)
    sync = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cattle} Tag Number: {self.tag_number} - Date: {self.tagging_date}"

    class Meta:
        db_table = 'tbl_cattle_tagging'
        verbose_name = 'Cattle Tagging'
        verbose_name_plural = 'Cattle Taggings'


class Symptoms(models.Model):
    symptom = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return self.symptom

    class Meta:
        db_table = 'tbl_animal_symptoms'
        verbose_name = 'Symptom'
        verbose_name_plural = 'Symptoms'


class Disease(models.Model):
    disease = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptoms, related_name="symptom_disease")
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return self.disease

    class Meta:
        db_table = 'tbl_animal_disease'
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'
    

class MedicineCategory(models.Model):
    category = models.CharField(max_length=100, unique=True)
    unit_of_quantity = models.CharField(max_length=20)
    sync = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.category} - {self.unit_of_quantity}'

    class Meta:
        db_table = 'tbl_medicine_category'
        verbose_name = 'Medicine Category'
        verbose_name_plural = 'Medicine Categories'


class Medicine(models.Model):
    medicine = models.CharField(max_length=100)
    description = models.TextField()
    expiary_date = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    recommended_for_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True, related_name="recommended_medicines")
    sync = models.BooleanField(default=False)

    def __str__(self):
        return self.medicine

    class Meta:
        db_table = 'tbl_medicine'
        verbose_name = 'Medicine'
        verbose_name_plural = 'Medicines'



class MedicineStock(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name="disease_medicines")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)
    sync = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medicine} - Stock Quantity: {self.stock_quantity}"

    class Meta:
        verbose_name = 'Medicine Stock'
        verbose_name_plural = 'Medicine Stocks'

    class Meta:
        db_table = 'tbl_medicine_stock'
        verbose_name = 'Medicine Stock'
        verbose_name_plural = 'Medicine Stock'

class DoctorMedicineStock(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="medicine_stocks")
    medicine_stock = models.ForeignKey(MedicineStock, on_delete=models.CASCADE)
    allocated_quantity = models.PositiveIntegerField(default=0)
    sync = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.username} - {self.medicine_stock}"

    class Meta:
        db_table = 'tbl_doc_medicine_stock'
        verbose_name = 'Doctor Medicine Stock'
        verbose_name_plural = 'Doctor Medicine Stocks'

class CattleCaseType(models.Model):
    NORMAL = 'Normal'
    SPECIAL = 'Special'
    OPERATIONAL = 'Operational'
    
    CASE_CHOICES = [
        (NORMAL, 'Normal'),
        (SPECIAL, 'Special'),
        (OPERATIONAL, OPERATIONAL),
    ]
    case_type = models.CharField(max_length=20, choices=CASE_CHOICES, default=NORMAL)
    sync = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.case_type}'

    class Meta:
        db_table = 'tbl_cattle_case_type'
        verbose_name = 'Case Type'
        verbose_name_plural = 'Case Types'


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    normal_cost = models.DecimalField(max_digits=10, decimal_places=2)
    operational_cost = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    sync = models.BooleanField(default=False)

    def __str__(self):
        time_slot = f'{self.start_time.strftime("%I:%M %p")} to {self.end_time.strftime("%I:%M %p")}' if self.end_time else f'{self.start_time.strftime("%I:%M %p")}'
        return f'{time_slot} - ${self.normal_cost}'
    
    class Meta:
        db_table = 'tbl_time_slot'
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'


class CattleCaseStatus(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    COMPLETED = 'Completed'
    
    STATUS_CHOICES = [
        (PENDING,PENDING),
        (CONFIRMED, CONFIRMED),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.status}'    
    
    class Meta:
        db_table = 'tbl_cattle_case_status'
        verbose_name = 'Case Status'
        verbose_name_plural = 'Case Statuses'

class DiagnosisCattleStatus(models.Model):
    MILKING = 'Milking'
    PREGNANT = 'Pregnant'
    DRY_CATTLE = 'Dry Cattle'
    
    STATUS_CHOICES = [
        (MILKING,MILKING),
        (PREGNANT, PREGNANT),
        (DRY_CATTLE, DRY_CATTLE),
    ]
    
    diagnosis_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.diagnosis_status}'    
    
    class Meta:
        db_table = 'tbl_diagnosis_status'
        verbose_name = 'Diagnosis Cattle Status'
        verbose_name_plural = 'Diagnosis Cattle Statuses'
    
import random
from django.db import models

class PaymentMethodChoices(models.TextChoices):
    ONLINE = 'online', 'Online'
    MILKBILLPAYMENT = 'milkbillpayment', 'Milk Bill Payment'

class PaymentMethod(models.Model):
    method = models.CharField(
        max_length=100,
        choices=PaymentMethodChoices.choices,
        unique=True
    )
    sync = models.BooleanField(default=False)

    def __str__(self):
        return self.get_method_display()

class OnlinePayment(models.Model):
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.CASCADE, primary_key=True, related_name='online_payment')
    gateway_name = models.CharField(max_length=100)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.gateway_name}"
    
    class Meta:
        db_table = 'tbl_online_payment_methods'
        verbose_name = 'Online Payment Method'
        verbose_name_plural = 'Online Payment Methods'

class DiagnosisRoute(models.Model):
    route = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.route}"

    class Meta:
        db_table = 'tbl_diagnosis_route'
        verbose_name = 'Diagnosis Route'
        verbose_name_plural = 'Diagnosis Routes'

class CaseEntry(models.Model):
    animal = models.ForeignKey(Cattle, on_delete=models.CASCADE, related_name='cattle_cases')
    applied_by_ext = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='case_by_ext', blank=True)
    applied_by_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_cases')
    status = models.ForeignKey(CattleCaseStatus, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, default="")
    remark = models.TextField(blank=True,null=True)
    advice = models.TextField(blank=True,null=True)
    case_no = models.CharField(max_length=250, primary_key=True)
    sync = models.BooleanField(default=False)

    def __str__(self):
        appliedby = self.applied_by_ext if self.applied_by_ext else self.applied_by_member
        return f'{self.case_no} - {appliedby}'    
    
    class Meta:
        db_table = 'tbl_case_entries'
        verbose_name = 'Case Entry'
        verbose_name_plural = 'Case Entries'

    def save(self, *args, **kwargs):
        if not self.case_no:
            farmer_code = self.animal.farmer.FarmerCode[-6:]
            if self.animal.tag_number:
                case_id = f'{farmer_code}{self.animal.tag_number}'
            else:
                random_number = random.randint(100, 999)
                case_id = f'{farmer_code}{random_number}'
            self.case_no = case_id
        super().save(*args, **kwargs)

class CaseReceiverLog(models.Model):
    case_entry = models.ForeignKey(CaseEntry, on_delete=models.CASCADE, related_name='receiver_logs', blank=True, null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transferred_at = models.DateTimeField(auto_now_add=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.receiver.username}'
    
    class Meta:
        db_table = 'tbl_case_reciever_logs'
        verbose_name = 'Case Receiver Log'
        verbose_name_plural = 'Case Receiver Logs'

class AnimalDiagnosis(models.Model):
    case_entry = models.ForeignKey(CaseEntry, on_delete=models.CASCADE, related_name='case_entry_diagnosis')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(DiagnosisCattleStatus, on_delete=models.SET_NULL, null=True)
    milk_production = models.CharField(max_length=100, blank=True, null=True)
    case_type = models.ForeignKey(CattleCaseType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.animal} - {self.disease.disease} - {self.created_at}"

    class Meta:
        db_table = 'tbl_animal_diagnosis'
        verbose_name = 'Animal Diagnosis'
        verbose_name_plural = 'Animal Diagnosis'

class DiagnosisSymptoms(models.Model):
    symptom = models.ForeignKey(Symptoms, on_delete=models.SET_NULL, null=True)
    diagnosis = models.ForeignKey(AnimalDiagnosis, on_delete=models.CASCADE, related_name="diagnosis_symptoms")
    remark  = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.diagnosis.disease.disease} - {self.created_at}"

    class Meta:
        db_table = 'tbl_animal_diagnosis_symp'
        verbose_name = 'Animal Diagnosis Symptom'
        verbose_name_plural = 'Animal Diagnosis Symptoms'
    
class AnimalTreatment(models.Model):
    case_treatment = models.ForeignKey(CaseEntry, on_delete=models.CASCADE, related_name="animal_treatment",blank=True, null=True)
    # doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="treatments_done")
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True)
    route = models.ForeignKey(DiagnosisRoute, on_delete=models.SET_NULL, null=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    sync = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.animal} - {self.disease} - {self.date}"

    class Meta:
        db_table = 'tbl_animal_treatments'
        verbose_name = 'Animal Treatment'
        verbose_name_plural = 'Animal Treatments'

class CasePayment(models.Model):
    case_entry = models.ForeignKey(CaseEntry, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.payment_method.online_payment:
            method = self.payment_method.online_payment.gateway_name
        else:
            method = self.payment_method.method
        return f"Payment for Case: {self.case_entry.case_no} - Amount: {self.amount} - Method: {method}"

    class Meta:
        db_table = 'tbl_case_payments'
        verbose_name = 'Case Payment'
        verbose_name_plural = 'Case Payments'

from math import radians, sin, cos, sqrt, atan2

class TravelRecord(models.Model):
    case_entry = models.OneToOneField(CaseEntry, on_delete=models.CASCADE, related_name="travel_records")
    from_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    from_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    to_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    to_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    distance_travelled = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Case Entry: {self.case_entry.case_no} - Distance Travelled: {self.distance_travelled} km - Date: {self.date}"

    class Meta:
        verbose_name = 'Travel Record'
        verbose_name_plural = 'Travel Records'

    def save(self, *args, **kwargs):
        if self.from_latitude and self.from_longitude and self.to_latitude and self.to_longitude:
            self.distance_travelled = self.calculate_distance()
        super().save(*args, **kwargs)

    def calculate_distance(self):
        from_lat = radians(float(self.from_latitude))
        from_lon = radians(float(self.from_longitude))
        to_lat = radians(float(self.to_latitude))
        to_lon = radians(float(self.to_longitude))
        R = 6371.0
        # Calculate the differences in latitude and longitude
        dlat = to_lat - from_lat
        dlon = to_lon - from_lon
        a = sin(dlat / 2)**2 + cos(from_lat) * cos(to_lat) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        return distance