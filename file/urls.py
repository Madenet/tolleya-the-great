from django.urls import path
from .views import *
# File uploads urls
path(
    "school/<slug>/documentations/upload/",
    handle_file_upload,
    name="upload_file_view",
),
path(
    "school/<slug>/documentations/<int:file_id>/edit/",
    handle_file_edit,
    name="upload_file_edit",
),
path(
    "school/<slug>/documentations/<int:file_id>/delete/",
    handle_file_delete,
    name="upload_file_delete",
),