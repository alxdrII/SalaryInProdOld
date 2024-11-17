from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'quota')
    list_display_links = ('code',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'hired', 'dismissed')
    list_display_links = ('fullname',)
    search_fields = ('dismissed', 'fullname',)


class BrigadeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'working', 'doc')
    list_display_links = ('employee',)
    # search_fields = ('doc', 'employee',)


class ProductionAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'doc')
    list_display_links = ('product',)
    # search_fields = ('doc',)


# Register your models here.
admin.site.register(Brigade, BrigadeAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(CreatedProducts)