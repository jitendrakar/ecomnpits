from django.contrib import admin
from .models import (
    ProductCategory, Brand, Product, ProductImage,
    ProductSpecification, Marketplace, ProductMarketplaceLink, MarketplaceClick
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 2


class ProductMarketplaceLinkInline(admin.TabularInline):
    model = ProductMarketplaceLink
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'brand', 'price', 'discount_price', 'stock_status', 'featured', 'is_active')
    list_filter = ('category', 'brand', 'stock_status', 'featured', 'is_active')
    search_fields = ('name', 'sku', 'description', 'short_description')
    list_editable = ('price', 'discount_price', 'stock_status', 'featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline, ProductMarketplaceLinkInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'brand', 'sku', 'stock_status', 'featured', 'is_active')
        }),
        ('Pricing & Warranty', {
            'fields': ('price', 'discount_price', 'warranty_period', 'warranty_type', 'warranty_details', 'warranty_terms')
        }),
        ('Descriptions & Media', {
            'fields': ('short_description', 'description', 'video_url')
        }),
        ('SEO Metadata', {
            'fields': ('seo_title', 'seo_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'base_url', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductMarketplaceLink)
class ProductMarketplaceLinkAdmin(admin.ModelAdmin):
    list_display = ('product', 'marketplace', 'url', 'is_active')
    list_filter = ('marketplace', 'is_active')
    search_fields = ('product__name', 'product__sku', 'url')


@admin.register(MarketplaceClick)
class MarketplaceClickAdmin(admin.ModelAdmin):
    list_display = ('product', 'marketplace', 'ip_address', 'created_at')
    list_filter = ('marketplace', 'created_at')
    readonly_fields = ('product', 'marketplace', 'ip_address', 'user_agent', 'created_at')
