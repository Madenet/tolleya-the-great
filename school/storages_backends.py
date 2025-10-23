from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'mediafiles'
    file_overwrite = False  # don’t overwrite files with the same name
