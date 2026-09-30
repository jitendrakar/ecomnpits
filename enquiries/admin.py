from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'service', 'product', 'location', 'source', 'status', 'created_at')
    list_filter = ('status', 'source', 'created_at', 'service')
    search_fields = ('customer_name', 'phone', 'email', 'location', 'message', 'calculation_details')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'phone', 'email', 'location')
        }),
        ('Lead Details', {
            'fields': ('source', 'status', 'service', 'product', 'preferred_date', 'preferred_time', 'message', 'attachment')
        }),
        ('Quotation / Calculation Breakdown', {
            'fields': ('calculation_details',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
