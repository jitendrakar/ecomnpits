from django.db import models
from django.utils.text import slugify


class ProductCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=150)
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    comparison_guide_html = models.TextField(blank=True, default="")
    comparison_guide_json = models.JSONField(blank=True, null=True, default=dict)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    STOCK_STATUS_CHOICES = [
        ('IN_STOCK', 'In Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('AVAILABLE_ON_ORDER', 'Available on Order'),
    ]

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    short_description = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Regular price in INR")
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Discounted price if available")
    stock_status = models.CharField(max_length=30, choices=STOCK_STATUS_CHOICES, default='IN_STOCK')
    warranty_period = models.CharField(max_length=100, default="1 Year", help_text="e.g. 1 Year, 3 Years, 6 Months")
    warranty_type = models.CharField(max_length=150, default="Manufacturer Warranty", help_text="e.g. On-Site, Carry-in, Dealer")
    warranty_details = models.TextField(blank=True, default="")
    warranty_terms = models.TextField(blank=True, default="")
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    video_url = models.URLField(max_length=500, blank=True, default="", help_text="YouTube video link for product tutorial/demo")
    seo_title = models.CharField(max_length=255, blank=True, default="")
    seo_description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        return self.discount_price if (self.discount_price and self.discount_price < self.price) else self.price

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    @property
    def youtube_embed_url(self):
        if not self.video_url:
            return ""
        url = self.video_url.strip()
        if "youtube.com/embed/" in url:
            return url
        if "youtube.com/watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True, default="")
    sort_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    specification_name = models.CharField(max_length=150)
    specification_value = models.CharField(max_length=255)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.specification_name}: {self.specification_value}"


class Marketplace(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    logo = models.ImageField(upload_to="marketplaces/", blank=True, null=True)
    base_url = models.URLField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductMarketplaceLink(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='marketplace_links')
    marketplace = models.ForeignKey(Marketplace, on_delete=models.CASCADE, related_name='product_links')
    url = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'marketplace')

    def __str__(self):
        return f"{self.product.name} on {self.marketplace.name}"


class MarketplaceClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Click: {self.product} -> {self.marketplace} at {self.created_at}"
