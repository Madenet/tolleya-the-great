from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import date
from django.db.models import Q
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.contrib.auth.validators import ASCIIUsernameValidator

# QuerySet for Bursary
class BursaryQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(summary__icontains=query) | Q(posted_as__icontains=query)
        return self.filter(lookups).distinct()

# Manager for Bursary
class BursaryManager(models.Manager):
    def get_queryset(self):
        return BursaryQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

# Bursary model
class Bursary(models.Model):
    POST_CHOICES = [
        ('funding', 'Funding'),
        ('Bursary', 'Bursary'),
        ('Loan', 'Loan'),
    ]

    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=20000, blank=True, null=True)
    website_url = models.CharField(max_length=2000, null=True, blank=True)
    picture = models.ImageField(upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True)
    posted_as = models.CharField(choices=POST_CHOICES, max_length=10)
    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    objects = BursaryManager()
    
    # Picture get
    def get_picture(self):
        try:
            return self.picture.url
        except:
            return settings.MEDIA_URL + "default.png"
    
    # Picture save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass
    
    # Picture delete
    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + "default.png":
            self.picture.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title