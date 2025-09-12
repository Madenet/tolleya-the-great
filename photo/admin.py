from django.contrib import admin
from .models import Photo
# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'approval_status', 'upload_date')
    list_filter = ('approval_status',)
    actions = ['approve_photos']

    def approve_photos(self, request, queryset):
        queryset.update(approval_status='approved')
    approve_photos.short_description = 'Approve selected photos'
