from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import SiteSettings, Testimonial, Page
from products.models import Product, ProductCategory, Brand
from services.models import Service, ServiceCategory, CCTVPricing
from enquiries.forms import EnquiryForm


def home_view(request):
    site_settings = SiteSettings.get_settings()
    featured_products = Product.objects.filter(is_active=True, featured=True).select_related('category', 'brand').prefetch_related('images', 'marketplace_links')[:6]
    if not featured_products.exists():
        featured_products = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images', 'marketplace_links')[:6]

    service_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
    featured_services = Service.objects.filter(is_active=True, featured=True).select_related('category')[:6]
    if not featured_services.exists():
        featured_services = Service.objects.filter(is_active=True).select_related('category')[:6]

    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:6]
    cctv_pricing = CCTVPricing.get_pricing()

    form = EnquiryForm(initial={'source': 'WEBSITE'})

    context = {
        'site_settings': site_settings,
        'featured_products': featured_products,
        'service_categories': service_categories,
        'featured_services': featured_services,
        'testimonials': testimonials,
        'cctv_pricing': cctv_pricing,
        'form': form,
    }
    return render(request, 'home.html', context)


def about_view(request):
    about_page = Page.objects.filter(slug='about', is_published=True).first()
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    context = {
        'about_page': about_page,
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)


def contact_view(request):
    site_settings = SiteSettings.get_settings()
    if request.method == 'POST':
        form = EnquiryForm(request.POST, request.FILES)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.source = 'CONTACT'
            enquiry.save()

            # Email notification logic
            try:
                subject = f"New Contact Enquiry from {enquiry.customer_name}"
                body = f"""New Enquiry Received:
Name: {enquiry.customer_name}
Phone: {enquiry.phone}
Email: {enquiry.email}
Location: {enquiry.location}
Message: {enquiry.message}
Source: {enquiry.get_source_display()}
"""
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Thank you! Your enquiry has been received. Our IT team will contact you shortly.")
            return redirect('enquiries:success')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = EnquiryForm(initial={'source': 'CONTACT'})

    context = {
        'site_settings': site_settings,
        'form': form,
    }
    return render(request, 'contact.html', context)


def page_detail_view(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'page_detail.html', {'page': page})


def robots_view(request):
    content = """User-agent: *
Allow: /
Sitemap: https://nehruplaceitservices.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


def sitemap_view(request):
    products = Product.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    pages = Page.objects.filter(is_published=True)

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    xml.append('<url><loc>https://nehruplaceitservices.com/</loc><priority>1.0</priority></url>')
    xml.append('<url><loc>https://nehruplaceitservices.com/products/</loc><priority>0.9</priority></url>')
    xml.append('<url><loc>https://nehruplaceitservices.com/services/</loc><priority>0.9</priority></url>')
    xml.append('<url><loc>https://nehruplaceitservices.com/services/cctv-calculator/</loc><priority>0.9</priority></url>')
    xml.append('<url><loc>https://nehruplaceitservices.com/about/</loc><priority>0.7</priority></url>')
    xml.append('<url><loc>https://nehruplaceitservices.com/contact/</loc><priority>0.8</priority></url>')

    for p in products:
        xml.append(f'<url><loc>https://nehruplaceitservices.com/products/{p.slug}/</loc><priority>0.8</priority></url>')

    for s in services:
        xml.append(f'<url><loc>https://nehruplaceitservices.com/services/{s.slug}/</loc><priority>0.8</priority></url>')

    for pg in pages:
        xml.append(f'<url><loc>https://nehruplaceitservices.com/page/{pg.slug}/</loc><priority>0.6</priority></url>')

    xml.append('</urlset>')
    return HttpResponse('\n'.join(xml), content_type="application/xml")


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def handler403(request, exception):
    return render(request, '403.html', status=403)


def health_check_view(request):
    return HttpResponse("OK", status=200, content_type="text/plain")

