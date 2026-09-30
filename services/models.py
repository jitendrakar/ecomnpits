from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=150)
    description = models.TextField(blank=True, default="")
    icon = models.CharField(max_length=50, default="bi-tools", help_text="Bootstrap icon class name, e.g. bi-laptop, bi-camera-video, bi-globe")
    image = models.ImageField(upload_to="services/categories/", blank=True, null=True)
    comparison_guide_html = models.TextField(blank=True, default="")
    comparison_guide_json = models.JSONField(blank=True, null=True, default=dict)
    is_active = models.BooleanField(default=True)

    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, max_length=200, db_index=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    short_description = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=50, default="per project", help_text="e.g. per project, per camera, per device")
    delivery_time = models.CharField(max_length=100, default="3-5 Days", help_text="e.g. Same Day, 3-5 Days")
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    seo_title = models.CharField(max_length=255, blank=True, default="")
    seo_description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=255)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.service.name} - {self.feature_text}"


class ServicePackage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    features = models.TextField(help_text="Enter features separated by line breaks")
    delivery_days = models.CharField(max_length=100, blank=True, default="")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'price']

    def __str__(self):
        return f"{self.service.name} - {self.name} (₹{self.price})"

    def feature_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class CCTVPricing(models.Model):
    camera_price = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00, help_text="Base unit cost per camera")
    dvr_nvr_price = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00, help_text="DVR/NVR device cost")
    hdd_price = models.DecimalField(max_digits=10, decimal_places=2, default=4000.00, help_text="Hard Disk Storage cost")
    power_supply_price = models.DecimalField(max_digits=10, decimal_places=2, default=800.00, help_text="Power supply box cost")
    connector_price = models.DecimalField(max_digits=10, decimal_places=2, default=300.00, help_text="BNC/DC connectors set")
    cable_price_per_meter = models.DecimalField(max_digits=10, decimal_places=2, default=25.00, help_text="CCTV Cable cost per meter")
    installation_charge = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00, help_text="Standard installation labor charge")
    wiring_charge_per_meter = models.DecimalField(max_digits=10, decimal_places=2, default=15.00, help_text="Wiring labor charge per meter")
    configuration_charge = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00, help_text="Network & Mobile App setup charge")
    maintenance_charge = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00, help_text="Optional AMC / Maintenance charge")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CCTV Pricing Configuration"
        verbose_name_plural = "CCTV Pricing Configuration"

    def __str__(self):
        return f"CCTV Pricing Config (Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    @classmethod
    def get_pricing(cls):
        pricing = cls.objects.first()
        if not pricing:
            pricing = cls.objects.create()
        return pricing


class CCTVPackage(models.Model):
    name = models.CharField(max_length=150)
    camera_count = models.IntegerField(default=4)
    camera_type = models.CharField(max_length=150, default="2MP HD Indoor/Outdoor Bullet")
    dvr_nvr = models.CharField(max_length=150, default="4 Channel HD DVR")
    storage = models.CharField(max_length=150, default="1 TB Hard Disk")
    cable_meters = models.IntegerField(default=100)
    installation_charge = models.DecimalField(max_digits=10, decimal_places=2, default=2000.00)
    wiring_charge = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    other_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    package_price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['package_price']

    def __str__(self):
        return f"{self.name} - ₹{self.package_price}"
