from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, ServiceCategory, CCTVPricing, CCTVPackage
from enquiries.forms import EnquiryForm


def service_list_view(request):
    category_slug = request.GET.get('category', '').strip()
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')

    services = Service.objects.filter(is_active=True).select_related('category').prefetch_related('features', 'packages')

    current_category = None
    if category_slug:
        current_category = get_object_or_404(ServiceCategory, slug=category_slug, is_active=True)
        services = services.filter(category=current_category)

    cctv_pricing = CCTVPricing.get_pricing()

    context = {
        'services': services,
        'categories': categories,
        'current_category': current_category,
        'cctv_pricing': cctv_pricing,
    }
    return render(request, 'services/service_list.html', context)


def service_detail_view(request, slug):
    service = get_object_or_404(
        Service.objects.select_related('category').prefetch_related('features', 'packages'),
        slug=slug,
        is_active=True
    )

    packages = service.packages.filter(is_active=True)
    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(id=service.id)[:4]

    enquiry_form = EnquiryForm(initial={
        'service': service,
        'source': 'SERVICE',
        'message': f"Hello, I am interested in your service: {service.name}. Please provide pricing details, availability, and delivery timeframe."
    })

    context = {
        'service': service,
        'packages': packages,
        'related_services': related_services,
        'enquiry_form': enquiry_form,
    }
    return render(request, 'services/service_detail.html', context)


def cctv_calculator_view(request):
    cctv_pricing = CCTVPricing.get_pricing()
    cctv_packages = CCTVPackage.objects.filter(is_active=True)

    if request.method == 'POST':
        form = EnquiryForm(request.POST, request.FILES)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.source = 'CCTV_CALCULATOR'
            cctv_service = Service.objects.filter(slug__icontains='cctv').first()
            if cctv_service:
                enquiry.service = cctv_service
            enquiry.save()

            # Email notification logic
            try:
                subject = f"New CCTV Quotation Request from {enquiry.customer_name}"
                body = f"""New CCTV Quote Request:
Name: {enquiry.customer_name}
Phone: {enquiry.phone}
Email: {enquiry.email}
Location: {enquiry.location}
Calculation Details:
{enquiry.calculation_details}
Message: {enquiry.message}
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

            messages.success(request, "Your CCTV quotation request has been submitted successfully! Our team will contact you with a customized setup plan.")
            return redirect('enquiries:success')
        else:
            messages.error(request, "Please fix the errors in the quote request form.")
    else:
        form = EnquiryForm(initial={
            'source': 'CCTV_CALCULATOR',
            'message': 'Please contact me regarding the CCTV installation calculation estimate.'
        })

    context = {
        'cctv_pricing': cctv_pricing,
        'cctv_packages': cctv_packages,
        'form': form,
    }
    return render(request, 'services/cctv_calculator.html', context)
