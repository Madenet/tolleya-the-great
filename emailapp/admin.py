from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','email_address','status')
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Option)