from django.contrib import admin
from django.http import HttpResponse
import csv
import xlsxwriter
from .models import *


class AwarenessAdmin(admin.ModelAdmin):
    search_fields = ['mpp__mpp_loc','leader_name']  # Assuming 'facilitator' and 'member' have a 'name' field
    list_display = ['id','mcc_name','mcc_code','mpp_name','mpp_code','leader_name','no_of_participants','created_at']
    
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
    
    def export_to_excelbook(self, request, queryset):
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="awareness_report.xlsx"'

            workbook = xlsxwriter.Workbook(response)
            worksheet = workbook.add_worksheet()

            # Write column headers
            headers = ['Id','MCC Code','MCC','MPP','MPP Code', 'Leader Name', 'No Of Participants', 'created_at']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            # Write data rows
            row = 1
            for obj in queryset:
                worksheet.write(row, 0, obj.id)
                worksheet.write(row, 1, obj.mpp.mcc.mcc)
                worksheet.write(row, 2, obj.mpp.mcc.mcc_code)
                worksheet.write(row, 3, obj.mpp.mpp_loc)
                worksheet.write(row, 4, obj.mpp.mpp_loc_code)
                worksheet.write(row, 5, obj.leader_name)
                worksheet.write(row, 6, obj.no_of_participants)
                worksheet.write(row, 7, obj.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                row += 1
            workbook.close()
            return response

    export_to_excelbook.short_description = "Export to xlsx"
    actions = ['export_to_excelbook']

admin.site.register(Awareness,AwarenessAdmin)


class AwarenessTeamMembersAdmin(admin.ModelAdmin):
    list_display = ['awareness','member_name','created_at']
    
    
admin.site.register(AwarenessTeamMembers,AwarenessTeamMembersAdmin)

class AwarenessImagesMembersAdmin(admin.ModelAdmin):
    list_display = ['awareness','image','created_at']
    
    
admin.site.register(AwarenessImages,AwarenessImagesMembersAdmin)