from django.db import models
from main_app.models import CustomUser
from job.models import Category
# Create your models here.


#Photos model
class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    APPROVAL_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    website_url = models.CharField(max_length=2000, null=True, blank=True)
    gmail_url = models.CharField(max_length=2000, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    facebook_url = models.CharField(max_length=300, null=True, blank=True)
    tiktok_url = models.CharField(max_length=300, null=True, blank=True)
    zoom_url = models.CharField(max_length=900, null=True, blank=True)
    microsoftTeam_url = models.CharField(max_length=900, null=True, blank=True)
    location = models.CharField(max_length=900, blank=True, null=True)
    twitter_url = models.CharField(max_length=900, null=True, blank=True)
    playstore_url = models.CharField(max_length=900, null=True, blank=True)
    linkedin_url = models.CharField(max_length=900, null=True, blank=True)
    instagram_url = models.CharField(max_length=900, null=True, blank=True)
    pinterest_url = models.CharField(max_length=900, null=True, blank=True)
    youtube_url = models.CharField(max_length=1000, null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    approval_status = models.CharField(
        max_length=10,
        choices=APPROVAL_STATUS,
        default='pending',  # New photos will be pending by default
    )

    def __str__(self):
        return self.description