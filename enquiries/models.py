from django.db import models
from products.models import Product
from services.models import Service


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    SOURCE_CHOICES = [
        ('WEBSITE', 'General Website'),
        ('PRODUCT', 'Product Page'),
        ('SERVICE', 'Service Page'),
        ('CCTV_CALCULATOR', 'CCTV Calculator'),
        ('CONTACT', 'Contact Page'),
        ('WHATSAPP', 'WhatsApp Link'),
    ]

    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50, db_index=True)
    email = models.EmailField(blank=True, default="")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    location = models.CharField(max_length=255, blank=True, default="")
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True, default="")
    message = models.TextField(blank=True, default="")
    attachment = models.FileField(upload_to="enquiries/attachments/", null=True, blank=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default='WEBSITE')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='NEW', db_index=True)
    calculation_details = models.TextField(blank=True, default="", help_text="Stored breakdown for CCTV calculator enquiries")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.customer_name} ({self.phone}) - {self.get_status_display()}"
