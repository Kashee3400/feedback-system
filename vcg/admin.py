from django.contrib import admin
from .models import *

from django.http import HttpResponse
import csv
import xlsxwriter


class FacilitatorAdmin(admin.ModelAdmin):
    search_fields = ['mcc__mcc', 'mcc__mcc_code', 'name']
    list_display = ['mcc_name', 'mcc_code', 'name']

    def mcc_name(self, obj):
        return obj.mcc.mcc if obj.mcc else None
    mcc_name.short_description = 'MCC'

    def mcc_code(self, obj):
        return obj.mcc.mcc_code if obj.mcc else None
    mcc_code.short_description = 'MCC Code'

admin.site.register(Facilitator, FacilitatorAdmin)

class ConductedTypeAdmin(admin.ModelAdmin):
    search_fields = ['conducted_type']
    list_display = ['conducted_type', 'date']
    
    def date(self, obj):
        return obj.created_dat if obj.created_dat else None
    date.short_description = 'Created At'

admin.site.register(ConductedByType,ConductedTypeAdmin)

class ConductedByNameAdmin(admin.ModelAdmin):
    search_fields = ['type__conducted_type','name']
    list_display = ['type', 'name','date']
    
    def date(self, obj):
        return obj.created_dat if obj.created_dat else None
    date.short_description = 'Created At'

admin.site.register(ConductedByName,ConductedByNameAdmin)

class VMembersAdmin(admin.ModelAdmin):
    search_fields = ['mpp__mpp_loc_code','mpp__mpp_loc','mpp__mcc__mcc','mpp__mcc__mcc_code','name']
    list_display = ['mcc_name', 'mcc_code','mpp_name','mpp_code','name','code','mineral_bag','cattle_bag','created_at']
    
    def mcc_name(self, obj):
        return obj.mpp.mcc.mcc if obj.mpp else None
    mcc_name.short_description = 'MCC'

    def mpp_name(self, obj):
        return obj.mpp.mpp_loc if obj.mpp else None
    mpp_name.short_description = 'MPP'
    
    def mcc_code(self, obj):
        return obj.mpp.mcc.mcc_code if obj.mpp else None
    mcc_code.short_description = 'MCC Code'

    def mpp_code(self, obj):
        return obj.mpp.mpp_loc_code if obj.mpp else None
    mpp_code.short_description = 'MPP Code'


admin.site.register(VMembers,VMembersAdmin)


class VCGMeetingAdmin(admin.ModelAdmin):
    search_fields = [
        'mpp__mpp_loc',
        'mpp__mcc__mcc',
        'mpp__mcc__mcc_code',
        'mpp__mpp_loc_code',
    ]
    list_display = [
        'meeting_id',
        'mcc_name',
        'mcc_code',
        'mpp_name',
        'mpp_code',
        'conducted_type',
        'conducted_by',
        'start_datetime',
        'end_datetime',
        'status'
    ]
    list_filter = ['status']
    
    def conducted_by(self, obj):
        if obj.conducted_by_fs:
            return obj.conducted_by_fs.name
        elif obj.conducted_by_name:
            return obj.conducted_by_name.name
        else: 
            return None
    conducted_by.short_description = 'Conducted By Name'

    def conducted_type(self, obj):
        return obj.conducted_by_type.conducted_type if obj.conducted_by_type else None
    conducted_type.short_description = 'Conducted By'
    
    def mcc_name(self, obj):
        return obj.mpp.mcc.mcc if obj.mpp and obj.mpp.mcc else None
    mcc_name.short_description = 'MCC'

    def mpp_name(self, obj):
        return obj.mpp.mpp_loc if obj.mpp else None
    mpp_name.short_description = 'MPP'
    
    def mcc_code(self, obj):
        return obj.mpp.mcc.mcc_code if obj.mpp and obj.mpp.mcc else None
    mcc_code.short_description = 'MCC Code'

    def mpp_code(self, obj):
        return obj.mpp.mpp_loc_code if obj.mpp else None
    mpp_code.short_description = 'MPP Code'

    def export_to_excelbook(self, request, queryset):
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="vcg_meeting_report.xlsx"'

            workbook = xlsxwriter.Workbook(response)
            worksheet = workbook.add_worksheet()

            # Write column headers
            headers = ['Meeting Id','MCC Code','MCC','MPP','MPP Code', 'Conducted By', 'Conducted By Name',
                       'Start Date','Start Time', 'End Date','End Time', 'Status']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            # Write data rows
            row = 1
            import pytz
            for obj in queryset:
                desired_timezone = pytz.timezone('Asia/Kolkata')
                start_datetime_local = obj.start_datetime.astimezone(desired_timezone)
                if obj.end_datetime:
                    end_datetime_local = obj.end_datetime.astimezone(desired_timezone)
                    end_date = end_datetime_local.strftime('%Y-%m-%d')
                    end_time = end_datetime_local.strftime('%I:%M %p')
                else:
                    end_date = ''
                    end_time=''
                if obj.conducted_by_fs:
                    name =  obj.conducted_by_fs.name
                elif obj.conducted_by_name:
                    name =  obj.conducted_by_name.name
                worksheet.write(row, 0, obj.meeting_id)
                worksheet.write(row, 1, obj.mpp.mcc.mcc)
                worksheet.write(row, 2, obj.mpp.mcc.mcc_code)
                worksheet.write(row, 3, obj.mpp.mpp_loc)
                worksheet.write(row, 4, obj.mpp.mpp_loc_code)
                worksheet.write(row, 5, obj.conducted_by_type.conducted_type)
                worksheet.write(row, 6, name)
                worksheet.write(row, 7,start_datetime_local.date().strftime('%Y-%m-%d'))
                worksheet.write(row, 8,start_datetime_local.time().strftime('%I:%M %p'))
                worksheet.write(row, 9, end_date)
                worksheet.write(row, 10, end_time)
                worksheet.write(row, 11, obj.status)
                row += 1
            workbook.close()
            return response

    export_to_excelbook.short_description = "Export to xlsx"
    actions = ['export_to_excelbook']

admin.site.register(VCGMeeting, VCGMeetingAdmin)

class VCGGroupAdmin(admin.ModelAdmin):
    list_display =  ['member']
    
admin.site.register(VCGroup, VCGGroupAdmin)

class VCGMemberAttendanceAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'member_name', 'member_code','status', 'date']
    list_select_related = ['member']  # To optimize database queries by performing a single JOIN

    def member_name(self, obj):
        return obj.member.member.name if obj.member else None
    member_name.short_description = 'Member Name'

    def member_code(self, obj):
        return obj.member.member.code if obj.member else None
    member_code.short_description = 'Member Code'

admin.site.register(VCGMemberAttendance, VCGMemberAttendanceAdmin)

class ZeroDaysReportAdmin(admin.ModelAdmin):
    list_display = ['member','reason','meeting']
    
admin.site.register(ZeroDaysPouringReport,ZeroDaysReportAdmin)

class ZeroDaysReasonAdmin(admin.ModelAdmin):
    list_display = ['reason']
    
admin.site.register(ZeroDaysPourerReason,ZeroDaysReasonAdmin)


class MemberComplaintReportAdmin(admin.ModelAdmin):
    list_display = ['member','reason','meeting']
    
admin.site.register(MemberComplaintReport,MemberComplaintReportAdmin)

class VCGImagesAdmin(admin.ModelAdmin):
    list_display = ['meeting','image','created_at']
    
admin.site.register(VCGMeetingImages,VCGImagesAdmin)

class VMPPAdmin(admin.ModelAdmin):
    list_display = ['mpp_loc','mpp_loc_code']
    search_fields = ['mcc__mcc','mcc__mcc_code','mpp_loc','mpp_loc_code']
    
admin.site.register(VMPPs,VMPPAdmin)


class VMccAdmin(admin.ModelAdmin):
    list_display = ['mcc','mcc_code']
    search_fields = ['mcc','mcc_code']
    
admin.site.register(VMCCs,VMccAdmin)


class MonthAssignmentAdmin(admin.ModelAdmin):
    list_display =['mpp','milk_collection','no_of_members','no_of_pourers','pourers_15_days','pourers_25_days','zero_days_pourers','cattle_feed_sale','mineral_mixture_sale','sahayak_recovery']
    search_fields = ['mpp__mpp_loc','mpp__mpp_loc_code']
    
admin.site.register(MonthAssignment,MonthAssignmentAdmin)


# Admin configuration for each model
class EventSessionAdmin(admin.ModelAdmin):
    list_display = ['session_name', 'created_at', 'updated_at']
    search_fields = ['session_name']
    ordering = ['-created_at']

class MppVisitByAdmin(admin.ModelAdmin):
    list_display = ['session','facilitator_name', 'mcc', 'mcc_code', 'mpp', 'mpp_name', 'no_of_pourer', 'no_of_non_member_pourer']
    search_fields = ['facilitator_name', 'mcc', 'mpp']

class CompositeDataAdmin(admin.ModelAdmin):
    list_display = ['session','qty', 'fat', 'snf', 'created_at']
    search_fields = ['qty', 'fat']

class DispatchDataAdmin(admin.ModelAdmin):
    list_display = ['session','qty', 'fat', 'snf', 'created_at']
    search_fields = ['qty', 'fat']

class MaintenanceChecklistAdmin(admin.ModelAdmin):
    list_display = ['session','battery_water_level', 'weekly_cleaning_done', 'created_at']
    search_fields = ['battery_water_level']

class NonPourerMeetAdmin(admin.ModelAdmin):
    list_display = ['session','member', 'cow_in_milk', 'cow_dry', 'buff_in_milk', 'buff_dry', 'surplus', 'created_at']
    search_fields = ['member__name']

class SessionVcgMeetingAdmin(admin.ModelAdmin):
    list_display = ['session','meeting_done', 'created_at']
    search_fields = ['meeting_done']

class MembershipAppAdmin(admin.ModelAdmin):
    list_display = ['session','no_of_installs', 'created_at']
    search_fields = ['no_of_installs']

class FormProgressAdmin(admin.ModelAdmin):
    list_display = ['session', 'step', 'status', 'timestamp']
    search_fields = ['session__session_name', 'step', 'status']

class ZeroPourerMembersAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'mpp', 'created_at']
    search_fields = ['mpp']

class AgriculturalProductsAdmin(admin.ModelAdmin):
    list_display = ['cf', 'mm', 'deverming', 'ss_utensils','fodder_seeds','created_at','updated_at']
    search_fields = ['cf', 'mm', 'deverming', 'ss_utensils','fodder_seeds']


# Register each model with its admin configuration
admin.site.register(AgriculturalProducts, AgriculturalProductsAdmin)
admin.site.register(EventSession, EventSessionAdmin)
admin.site.register(MppVisitBy, MppVisitByAdmin)
admin.site.register(CompositeData, CompositeDataAdmin)
admin.site.register(DispatchData, DispatchDataAdmin)
admin.site.register(MaintenanceChecklist, MaintenanceChecklistAdmin)
admin.site.register(NonPourerMeet, NonPourerMeetAdmin)
admin.site.register(SessionVcgMeeting, SessionVcgMeetingAdmin)
admin.site.register(MembershipApp, MembershipAppAdmin)
admin.site.register(FormProgress, FormProgressAdmin)
admin.site.register(ZeroPourerMembers, ZeroPourerMembersAdmin)
