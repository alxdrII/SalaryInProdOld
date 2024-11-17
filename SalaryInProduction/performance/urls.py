from django.urls import path
from .views import perf_main, perf_doc_show, dict_view


urlpatterns = [
    path('', perf_main),
    path('doc_show/', perf_doc_show),
    path('dicts/', dict_view),
]