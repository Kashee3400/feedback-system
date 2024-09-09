from django import forms
from .models import MppVisitBy, CompositeData, DispatchData, MaintenanceChecklist, NonPourerMeet, MembershipApp, SessionVcgMeeting, ZeroPourerMembers

class MppVisitByForm(forms.ModelForm):
    class Meta:
        model = MppVisitBy
        fields = ['facilitator_name', 'mcc', 'mcc_code', 'mpp', 'mpp_name', 'no_of_pourer', 'no_of_non_member_pourer', 'sahayak_code', 'non_pourer_names']
        widgets = {
            'facilitator_name': forms.TextInput(attrs={"data-role":"input"}),
            'mcc_code': forms.TextInput(attrs={"data-role":"input"}),
            'mcc': forms.TextInput(attrs={"data-role":"input"}),
            'mpp': forms.TextInput(attrs={"data-role":"input"}),
            'mpp_name': forms.TextInput(attrs={"data-role":"input"}),
            'no_of_pourer': forms.NumberInput(attrs={"data-role":"input"}),
            'no_of_non_member_pourer': forms.NumberInput(attrs={"data-role":"input"}),
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
            'sahayak_code': 'In which code sahayak pouring milk',
            'non_pourer_names': 'Non-Pourer Names',
        }

    def clean(self):
        cleaned_data = super().clean()
        no_of_non_pourer_member = int(cleaned_data.get('no_of_non_member_pourer'))
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
            'battery_water_level': 'Battery Water Level',
            'weekly_cleaning_done': 'Weekly Cleaning Done',
        }
class NonPourerMeetForm(forms.ModelForm):

    class Meta:
        model = NonPourerMeet
        fields = ['member', 'cow_in_milk', 'cow_dry', 'buff_in_milk', 'buff_dry', 'surplus','reason']
        widgets = {
            'member': forms.Select(attrs={'data-role':'select'}),
            'cow_in_milk': forms.NumberInput(attrs={"data-role": "input",}),
            'cow_dry': forms.NumberInput(attrs={"data-role": "input",}),
            'buff_in_milk': forms.NumberInput(attrs={"data-role": "input",}),
            'buff_dry': forms.NumberInput(attrs={"data-role": "input",}),
            'surplus': forms.NumberInput(attrs={"data-role": "input",}),
            'reason':forms.Textarea(attrs={"data-role":"textarea", "data-prepend":"<span class='mif-leanpub'></span>"})
        }
        labels = {
            'member': 'Member',
            'cow_in_milk': 'Cows in Milk',
            'cow_dry': 'Dry Cows',
            'buff_in_milk': 'Buffaloes in Milk',
            'buff_dry': 'Dry Buffaloes',
            'surplus': 'Surplus',
            'reason': 'Reason'
        }
        
    def __init__(self, *args, **kwargs):
        mpp = kwargs.pop('mpp', None)
        super().__init__(*args, **kwargs)
        if mpp:
            queryset = ZeroPourerMembers.objects.filter(mpp=mpp)
        else:
            queryset = ZeroPourerMembers.objects.all()

        self.fields['member'].queryset = queryset

    def clean(self):
        cleaned_data = super().clean()

        cow_in_milk = cleaned_data.get('cow_in_milk')
        buff_in_milk = cleaned_data.get('buff_in_milk')
        surplus = cleaned_data.get('surplus')
        reason = cleaned_data.get('reason')

        # Condition 1: Check if both cow_in_milk and buff_in_milk are 0
        if (cow_in_milk == 0 or cow_in_milk is None) and (buff_in_milk == 0 or buff_in_milk is None):
            if surplus and surplus > 0:
                self.add_error('surplus', 'Surplus can\'t be more than 0 when both cows and buffaloes are not producing milk.')

        # Condition 2: Check if surplus is greater than 0 and reason is not provided
        if surplus and surplus > 0 and not reason:
            self.add_error('reason', 'Reason is required when surplus is greater than 0.')

        return cleaned_data

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
