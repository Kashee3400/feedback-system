from django.contrib import admin
from django.http import HttpResponse
import csv
import xlsxwriter
from .models import *
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.contrib.admin import SimpleListFilter
from django.db.models import Count

class HasImagesFilter(SimpleListFilter):
    title = 'Images'
    parameter_name = 'has_images'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        no_images_count = queryset.annotate(num_images=Count('awareness_images')).filter(num_images=0).count()
        has_images_count = queryset.annotate(num_images=Count('awareness_images')).filter(num_images__gt=0).count()

        return (
            ('yes', f'Yes ({has_images_count})'),
            ('no', f'No ({no_images_count})'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.annotate(num_images=Count('awareness_images')).filter(num_images__gt=0)
        if self.value() == 'no':
            return queryset.annotate(num_images=Count('awareness_images')).filter(num_images=0)
        return queryset

class AwarenessAdmin(admin.ModelAdmin):
    search_fields = [
        'mpp__mpp_loc',
        'mpp__mcc__mcc',
        'mpp__mcc__mcc_code',
        'mpp__mpp_loc_code',
    ]
        
    list_display = ['id','mcc_name','mcc_code','mpp_name','mpp_code','leader_name','no_of_participants','created_at']
    # list_filter = ['status']
    list_filter = [HasImagesFilter]  # Add the custom filter here
    
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
            headers = ['Id','MCC Code','MCC','MPP','MPP Code', 'Leader Name', 'No Of Participants', 'Date', 'Time']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            # Write data rows
            row = 1
            import pytz
            desired_timezone = pytz.timezone('Asia/Kolkata')
            
            for obj in queryset:
                start_datetime_local = obj.created_at.astimezone(desired_timezone)
                worksheet.write(row, 0, obj.id)
                worksheet.write(row, 1, obj.mpp.mcc.mcc)
                worksheet.write(row, 2, obj.mpp.mcc.mcc_code)
                worksheet.write(row, 3, obj.mpp.mpp_loc)
                worksheet.write(row, 4, obj.mpp.mpp_loc_code)
                worksheet.write(row, 5, obj.leader_name)
                worksheet.write(row, 6, obj.no_of_participants)
                worksheet.write(row, 7, start_datetime_local.strftime('%Y-%m-%d'))
                worksheet.write(row, 8, start_datetime_local.strftime('%I:%M %p'))
                row += 1
            workbook.close()
            return response
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_images=Count('awareness_images'))
        return queryset

    def fetch_awareness_without_images(self, request, queryset):
        queryset = self.get_queryset(request).filter(num_images=0)
        self.message_user(request, f"Found {queryset.count()} awareness records without images.")
        return HttpResponseRedirect(request.get_full_path())
    fetch_awareness_without_images.short_description = "Fetch Awareness without images"

    export_to_excelbook.short_description = "Export to xlsx"
    actions = ['export_to_excelbook','fetch_awareness_without_images']

admin.site.register(Awareness,AwarenessAdmin)


class AwarenessTeamMembersAdmin(admin.ModelAdmin):
    list_display = ['awareness','member_name','created_at']
    
    
admin.site.register(AwarenessTeamMembers,AwarenessTeamMembersAdmin)

class AwarenessImagesMembersAdmin(admin.ModelAdmin):
    list_display = ['awareness','image','created_at']
    
    
admin.site.register(AwarenessImages,AwarenessImagesMembersAdmin)

