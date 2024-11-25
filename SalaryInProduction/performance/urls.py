from django.urls import path
from .views import *


urlpatterns = [
    path('', perf_main),
    path('doc_show/<int:doc_id>', perf_doc_show),
    path('dicts/works/', works_view, name="employees_list"),
    path('dicts/prods/', prods_view, name="products_list"),
    path('dicts/', dicts_view),
    path('report/', report_view),
    path('edit_empl/<int:empl_id>/', edit_employee),
    path('edit_prod/<int:prod_id>/', edit_product),
]