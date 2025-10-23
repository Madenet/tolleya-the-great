# upload_test.py
import os
import django

# tell Django where your settings.py is
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")  # <-- replace with your settings module path

django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

try:
    name = default_storage.save("test_s3_upload.txt", ContentFile("Hello, AWS from Django!"))
    print("✅ Uploaded:", name)
except Exception as e:
    print("❌ Error:", e)
