from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import EnquiryForm


def submit_enquiry_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST, request.FILES)
        if form.is_valid():
            enquiry = form.save()
            try:
                subject = f"New Enquiry from {enquiry.customer_name} ({enquiry.get_source_display()})"
                body = f"""New Enquiry Received:
Name: {enquiry.customer_name}
Phone: {enquiry.phone}
Email: {enquiry.email}
Service: {enquiry.service.name if enquiry.service else 'N/A'}
Product: {enquiry.product.name if enquiry.product else 'N/A'}
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

            messages.success(request, "Your enquiry has been submitted successfully! Our team will contact you shortly.")
            return redirect('enquiries:success')
        else:
            messages.error(request, "Error submitting enquiry. Please check your input and try again.")
            return redirect(request.META.get('HTTP_REFERER', 'core:home'))

    return redirect('core:home')


def success_view(request):
    return render(request, 'enquiries/success.html')
