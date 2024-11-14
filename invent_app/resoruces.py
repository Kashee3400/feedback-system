from import_export import resources
from .models import *

class FarmerFeedbacksResource(resources.ModelResource):

    class Meta:
        model = FarmerFeedback
        fields = ('feedback_id','mcc_code', 'mcc_ex_code', 'mcc_name', 'mpp_code', 'mpp_short_name','name','code', 'mobile', 'message','is_closed','created_at')
        exclude = ('id',)
        import_id_fields = ('mpp_code', 'mcc_code')
        
