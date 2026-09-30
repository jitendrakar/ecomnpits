from django.contrib import admin
from .models import SiteSettings, Testimonial, Page


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'whatsapp_number')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'company', 'rating', 'is_featured', 'is_active', 'created_at')
    list_filter = ('rating', 'is_featured', 'is_active')
    search_fields = ('customer_name', 'company', 'review')
    list_editable = ('is_featured', 'is_active')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
