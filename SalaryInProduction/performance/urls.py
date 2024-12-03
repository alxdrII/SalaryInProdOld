from django.urls import path
from .views import *


urlpatterns = [
    path('', perf_main, name='docs_list'),
    path('doc_show/<int:doc_id>', perf_doc_show, name='perf_doc'),
    path('dicts/works/', works_view, name="employees_list"),
    path('dicts/prods/', prods_view, name="products_list"),
    path('dicts/', dicts_view, name='menu_lists'),
    path('report/', report_view, name='report'),
    path('edit_empl/<int:empl_id>/', edit_employee, name='edit_employee'),
    path('edit_prod/<int:prod_id>/', edit_product, name='edit_product'),
]