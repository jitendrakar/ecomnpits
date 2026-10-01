from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=150, default="Nehru Place IT Services")
    tagline = models.CharField(max_length=255, default="Smart IT Solutions for Modern Business")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    phone = models.CharField(max_length=50, default="+91 9871808718")
    alternate_phone = models.CharField(max_length=50, blank=True, default="+91 8287595989")
    email = models.EmailField(default="info@npits.in")
    whatsapp_number = models.CharField(max_length=20, default="919871808718", help_text="Number in international format without + sign, e.g. 919871808718")
    address = models.TextField(default="Nehru Place, New Delhi, Delhi 110019")
    google_map_url = models.URLField(blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    about_text = models.TextField(blank=True, default="Nehru Place IT Services is your one-stop solution for IT products, custom website development, CCTV security installations, networking setup, and expert hardware repair.")
    footer_text = models.TextField(blank=True, default="Empowering businesses with top-tier technology, responsive web applications, robust security systems, and reliable IT maintenance.")
    default_meta_title = models.CharField(max_length=255, default="Nehru Place IT Services | IT Products, Web Dev, CCTV & Support")
    default_meta_description = models.TextField(default="Leading provider of IT products, website development, CCTV installation, networking, and laptop repair services in Nehru Place.")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.company_name

    @classmethod
    def get_settings(cls):
        settings = cls.objects.first()
        if not settings:
            settings = cls.objects.create()
        return settings


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, blank=True, default="")
    designation = models.CharField(max_length=100, blank=True, default="")
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    rating = models.IntegerField(default=5)
    review = models.TextField()
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField(help_text="HTML content allowed")
    seo_title = models.CharField(max_length=255, blank=True, default="")
    seo_description = models.TextField(blank=True, default="")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Update Subscriber"
        verbose_name_plural = "Product Update Subscribers"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
