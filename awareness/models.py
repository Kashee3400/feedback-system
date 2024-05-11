from django.db import models
from vcg.models import VMPPs


class Awareness(models.Model):
    mpp = models.ForeignKey(VMPPs, on_delete=models.SET_NULL,null=True, related_name='mpp_awareness')
    no_of_participants = models.IntegerField(default=0, help_text='No of Members')
    leader_name = models.CharField(max_length=100, help_text='Team Leader Name')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Awareness #{self.pk} {self.leader_name}'

    class Meta:
        db_table = 'tbl_awareness'
        verbose_name = 'Awareness'
        verbose_name_plural = 'Awarenesse'


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

