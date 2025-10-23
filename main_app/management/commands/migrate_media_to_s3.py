import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Uploads all local media files to S3 preserving folder structure'

    def handle(self, *args, **options):
        # Update this path to your local media root
        LOCAL_MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'static/mediafiles')


        if not os.path.exists(LOCAL_MEDIA_ROOT):
            self.stdout.write(self.style.ERROR(f"Local media root does not exist: {LOCAL_MEDIA_ROOT}"))
            return

        self.stdout.write(f"Starting migration from {LOCAL_MEDIA_ROOT} to S3...")

        count = 0
        for root, dirs, files in os.walk(LOCAL_MEDIA_ROOT):
            for f in files:
                local_path = os.path.join(root, f)
                relative_path = os.path.relpath(local_path, LOCAL_MEDIA_ROOT)
                try:
                    with open(local_path, "rb") as file_data:
                        default_storage.save(relative_path, file_data)
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Uploaded: {relative_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to upload {relative_path}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Migration completed! {count} files uploaded to S3."))