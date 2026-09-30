from django.contrib import admin
from .models import ServiceCategory, Service, ServiceFeature, ServicePackage, CCTVPricing, CCTVPackage


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 2


class ServicePackageInline(admin.StackedInline):
    model = ServicePackage
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'starting_price', 'price_unit', 'featured', 'is_active')
    list_filter = ('category', 'featured', 'is_active')
    search_fields = ('name', 'description', 'short_description')
    list_editable = ('starting_price', 'featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceFeatureInline, ServicePackageInline]


@admin.register(CCTVPricing)
class CCTVPricingAdmin(admin.ModelAdmin):
    list_display = ('camera_price', 'dvr_nvr_price', 'hdd_price', 'cable_price_per_meter', 'installation_charge', 'wiring_charge_per_meter', 'updated_at')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CCTVPackage)
class CCTVPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'camera_count', 'package_price', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('package_price', 'is_active')
