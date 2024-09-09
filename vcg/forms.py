from django import forms
from .models import MppVisitBy, CompositeData, DispatchData, MaintenanceChecklist, NonPourerMeet, MembershipApp, SessionVcgMeeting, ZeroPourerMembers

class MppVisitByForm(forms.ModelForm):
    class Meta:
        model = MppVisitBy
        fields = ['facilitator_name', 'mcc', 'mcc_code', 'mpp', 'mpp_name', 'no_of_pourer', 'no_of_non_member_pourer', 'non_pourer_names','sahayak_code','new_membership_enrolled']
        widgets = {
            'facilitator_name': forms.TextInput(attrs={"data-role":"input"}),
            'mcc_code': forms.TextInput(attrs={"data-role":"input"}),
            'mcc': forms.TextInput(attrs={"data-role":"input"}),
            'mpp': forms.TextInput(attrs={"data-role":"input"}),
            'mpp_name': forms.TextInput(attrs={"data-role":"input"}),
            'no_of_pourer': forms.NumberInput(attrs={"data-role":"input"}),
            'no_of_non_member_pourer': forms.NumberInput(attrs={"data-role":"input"}),
            'new_membership_enrolled': forms.NumberInput(attrs={"data-role":"input"}),
            'non_pourer_names': forms.Textarea(attrs={"data-role":"taginput", "data-tag-trigger":"Comma"}),
            'sahayak_code': forms.TextInput(attrs={"data-role":"taginput", "data-tag-trigger":"Comma"}),
        }
        labels = {
            'facilitator_name': 'Facilitator Name',
            'mcc': 'MCC Name',
            'mcc_code': 'MCC Code',
            'mpp': 'MPP Code',
            'mpp_name': 'MPP Name',
            'no_of_pourer': 'Number of Pourers',
            'no_of_non_member_pourer': 'Number of Non-Members Pourer',
            'sahayak_code': 'In which code sahayak pouring non-member milk',
            'non_pourer_names': 'Non-Member Names',
        }

    def clean(self):
        cleaned_data = super().clean()
        no_of_non_pourer_member = cleaned_data.get('no_of_non_member_pourer')
        sahayak_code = cleaned_data.get('sahayak_code')
        non_pourer_names = cleaned_data.get('non_pourer_names')

        # Validate sahayak_code and non_pourer_names when no_of_non_pourer_member is greater than 0
        if no_of_non_pourer_member and no_of_non_pourer_member > 0:
            if not sahayak_code:
                self.add_error('sahayak_code', 'Pouring code is required when there are non-pourer members.')
            if not non_pourer_names:
                self.add_error('non_pourer_names', 'Non-pourer names are required when there are non-pourer members.')

        return cleaned_data

class CompositeDataForm(forms.ModelForm):
    class Meta:
        model = CompositeData
        fields = ['qty', 'fat', 'snf']
        widgets = {
            'qty': forms.NumberInput(attrs={"data-role":"input",}),
            'fat': forms.NumberInput(attrs={"data-role":"input",}),
            'snf': forms.NumberInput(attrs={"data-role":"input",}),
        }
        labels = {
            'qty': 'Composite Quantity',
            'fat': 'Composite Fat',
            'snf': 'Composite SNF',
        }

class DispatchDataForm(forms.ModelForm):
    class Meta:
        model = DispatchData
        fields = ['qty', 'fat', 'snf']
        widgets = {
            'qty': forms.NumberInput(attrs={"data-role":"input",}),
            'fat': forms.NumberInput(attrs={"data-role":"input",}),
            'snf': forms.NumberInput(attrs={"data-role":"input",}),
        }
        labels = {
            'qty': 'Dispatch Quantity',
            'fat': 'Dispatch Fat',
            'snf': 'Dispatch SNF',
        }

class MaintenanceChecklistForm(forms.ModelForm):
    class Meta:
        model = MaintenanceChecklist
        fields = ['battery_water_level', 'weekly_cleaning_done']
        widgets = {
            'battery_water_level': forms.CheckboxInput(attrs={"type": "checkbox", "data-role": "switch", "data-material": "true"}),
            'weekly_cleaning_done': forms.CheckboxInput(attrs={"type": "checkbox", "data-role": "switch", "data-material": "true"}),
        }
        labels = {
            'battery_water_level': 'Battery Water Level Check',
            'weekly_cleaning_done': 'Weekly Cleaning Done',
        }

class MembershipAppForm(forms.ModelForm):
    class Meta:
        model = MembershipApp
        fields = ['no_of_installs']
        widgets = {
            'no_of_installs': forms.NumberInput(attrs={"data-role":"input",}),
        }
        labels = {
            'no_of_installs': 'Number of Membership Application Installed',
        }

class VcgMeetingForm(forms.ModelForm):
    class Meta:
        model = SessionVcgMeeting
        fields = ['meeting_done']
        widgets = {
            'meeting_done': forms.CheckboxInput(attrs={"type": "checkbox", "data-role": "switch", "data-material": "true"}),
        }
        labels = {
            'meeting_done': 'Meeting Done',
        }

from .models import AgriculturalProducts

class ProductsDemandsForm(forms.ModelForm):
    
    class Meta:
        model = AgriculturalProducts
        fields = ['cf', 'mm', 'deverming', 'ss_utensils', 'fodder_seeds']
        widgets = {
            'cf': forms.NumberInput(attrs={'type':'text',"data-role":"input", 'min': 0, 'step': 1}),
            'mm': forms.NumberInput(attrs={'type':'text',"data-role":"input", 'min': 0, 'step': 1}),
            'deverming': forms.NumberInput(attrs={'type':'text',"data-role":"input", 'min': 0, 'step': 1}),
            'ss_utensils': forms.NumberInput(attrs={'type':'text',"data-role":"input", 'min': 0, 'step': 1}),
            'fodder_seeds': forms.NumberInput(attrs={'type':'text',"data-role":"input", 'min': 0, 'step': 1}),
        }


from django import forms
from .models import NonPourerMeet, ZeroPourerMembers, ZeroDaysPourerReason

class NonPourerMeetForm(forms.ModelForm):
    class Meta:
        model = NonPourerMeet
        fields = [
            'member', 'cow_in_milk', 'cow_dry', 'buff_in_milk',
            'buff_dry', 'surplus', 'zero_days_reaason', 'reason'
        ]
        widgets = {
            'member': forms.Select(attrs={'data-role': 'select'}),
            'cow_in_milk': forms.NumberInput(attrs={"data-role": "input"}),
            'cow_dry': forms.NumberInput(attrs={"data-role": "input"}),
            'buff_in_milk': forms.NumberInput(attrs={"data-role": "input"}),
            'buff_dry': forms.NumberInput(attrs={"data-role": "input"}),
            'surplus': forms.NumberInput(attrs={"data-role": "input"}),
            'zero_days_reaason': forms.Select(attrs={'data-role': 'select'}),
            'reason': forms.Textarea(attrs={"data-role": "textarea", "data-prepend": "<span class='mif-leanpub'></span>"})
        }
        labels = {
            'member': 'Member',
            'cow_in_milk': 'Cows in Milk',
            'cow_dry': 'Dry Cows',
            'buff_in_milk': 'Buffaloes in Milk',
            'buff_dry': 'Dry Buffaloes',
            'surplus': 'Surplus',
            'zero_days_reaason': 'Zero Days Reason',
            'reason': 'Other Reason'
        }
        
    def __init__(self, *args, **kwargs):
        mpp = kwargs.pop('mpp', None)
        super().__init__(*args, **kwargs)
        if mpp:
            queryset = ZeroPourerMembers.objects.filter(mpp=mpp)
        else:
            queryset = ZeroPourerMembers.objects.all()            
        self.fields['member'].queryset = queryset


    def clean_cow_in_milk(self):
        cow_in_milk = self.cleaned_data.get('cow_in_milk')
        if cow_in_milk is not None and cow_in_milk < 0:
            raise forms.ValidationError("Cows in milk cannot be negative.")
        return cow_in_milk

    def clean_cow_dry(self):
        cow_dry = self.cleaned_data.get('cow_dry')
        if cow_dry is not None and cow_dry < 0:
            raise forms.ValidationError("Dry cows cannot be negative.")
        return cow_dry

    def clean_buff_in_milk(self):
        buff_in_milk = self.cleaned_data.get('buff_in_milk')
        if buff_in_milk is not None and buff_in_milk < 0:
            raise forms.ValidationError("Buffaloes in milk cannot be negative.")
        return buff_in_milk

    def clean_buff_dry(self):
        buff_dry = self.cleaned_data.get('buff_dry')
        if buff_dry is not None and buff_dry < 0:
            raise forms.ValidationError("Dry buffaloes cannot be negative.")
        return buff_dry

    def clean_surplus(self):
        surplus = self.cleaned_data.get('surplus')
        cow_in_milk = self.cleaned_data.get('cow_in_milk')
        buff_in_milk = self.cleaned_data.get('buff_in_milk')
        
        if (cow_in_milk == 0 or cow_in_milk is None) and (buff_in_milk == 0 or buff_in_milk is None):
            if surplus is not None and surplus > 0:
                raise forms.ValidationError("Surplus can’t be more than 0 when both cows and buffaloes are not producing milk.")
        return surplus

    def clean_reason(self):
        reason = self.cleaned_data.get('reason')
        zero_days_reaason = self.cleaned_data.get('zero_days_reaason')

        if zero_days_reaason == 'Others' and not reason:
            raise forms.ValidationError("Reason is required when the zero days reason is 'Others'.")
        
        return reason

