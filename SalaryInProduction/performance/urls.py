from django.urls import path
from .views import *


urlpatterns = [
    path('', perf_main),
    path('doc_show/', perf_doc_show),
    path('dicts/works/', works_view),
    path('dicts/prods/', prods_view),
    path('dicts/', dicts_view),
    path('report/', report_view)
]