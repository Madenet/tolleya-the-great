from django.db import models
from main_app.models import CustomUser
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.
#Category model
class University(models.Model):
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universitys'

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

#application GameChanger
class Application(models.Model):
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    details = models.TextField(max_length=2000, null=True, blank=True)
    disability = models.TextField(max_length=2000, null=True, blank=True)
    student = models.CharField(max_length=2000, null=True, blank=True)
    address = models.CharField(max_length=2000, null=True, blank=True)
    bursary = models.CharField(max_length=2000, null=True, blank=True)
    varsity = models.TextField(max_length=2000, null=True, blank=True)
    upload_date = models.DateTimeField( default=timezone.now)
    keen = models.CharField(max_length=2000, null=True, blank=True)
   
    def __str__(self):
        return self.keen
    

    
