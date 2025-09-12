from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from decimal import Decimal
from main_app.models import CustomUser

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email_address = models.EmailField()
    customer_status = (('active', 'active',),('inactive','inactive'))
    status = models.CharField(max_length=50,choices=customer_status,default='active')
    
    def __str__(self):
        return self.name


class Option(models.Model):
    APPLICATION_CHOICES = [
        ('school', 'School'),
        ('individual', 'Individual'),
    ]

    Full_Names = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    option_date = models.DateTimeField(default=timezone.now)
    Where_to_Apply = models.TextField(max_length=255)
    header_image = models.ImageField(upload_to='images/')
    image = models.ImageField(upload_to="carousel/%Y/%m/%d/", blank=True, null=True, default='/static/img/default-user.png')
    application_from = models.CharField(max_length=10, choices=APPLICATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.Full_Names

    def calculate_total_price(self):
        """
        Calculates the total price based on the user-entered price and the pricing rules.
        """
        base_price = Decimal('50.00')  # Define base price as a Decimal object

        if self.price <= Decimal('250.00'):
            return self.price + base_price
        elif self.price <= Decimal('400.00'):
            return self.price + base_price + Decimal('100.00')
        else:
            return self.price + base_price + Decimal('150.00')

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)