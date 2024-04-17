from ecommerce_app.models import *
from ecommerce_api.serializers import *

PRODUCT_TYPE_MAPPING = {
    'ElectronicProduct': {
        'model': ElectronicProduct,
        'serializer': ElectronicProductSerializer,
    },
    'FashionProduct': {
        'model': FashionProduct,
        'serializer': FashionProductSerializer,
    },
    'BookProduct': {
        'model': BookProduct,
        'serializer': BookProductSerializer,
    },
}
