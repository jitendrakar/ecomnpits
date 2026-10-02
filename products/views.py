from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, ProductCategory, Brand, ProductMarketplaceLink, MarketplaceClick
from enquiries.forms import EnquiryForm


def product_list_view(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images', 'marketplace_links')

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    brand_slug = request.GET.get('brand', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    warranty = request.GET.get('warranty', '').strip()
    stock = request.GET.get('stock', '').strip()
    sort = request.GET.get('sort', 'newest').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(specifications__specification_name__icontains=query) |
            Q(specifications__specification_value__icontains=query)
        ).distinct()

    current_category = None
    if category_slug:
        current_category = get_object_or_404(ProductCategory, slug=category_slug, is_active=True)
        products = products.filter(category=current_category)

    current_brand = None
    if brand_slug:
        current_brand = get_object_or_404(Brand, slug=brand_slug, is_active=True)
        products = products.filter(brand=current_brand)

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if warranty:
        products = products.filter(warranty_period__icontains=warranty)

    if stock:
        products = products.filter(stock_status=stock)

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = ProductCategory.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    context = {
        'products': page_obj,
        'categories': categories,
        'brands': brands,
        'current_category': current_category,
        'current_brand': current_brand,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'warranty': warranty,
        'stock': stock,
        'sort': sort,
        'total_count': products.count(),
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related(
            'images', 'specifications', 'marketplace_links__marketplace'
        ),
        slug=slug,
        is_active=True
    )

    marketplace_links = product.marketplace_links.filter(is_active=True, marketplace__is_active=True).select_related('marketplace')

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('category', 'brand').prefetch_related('images')[:4]

    enquiry_form = EnquiryForm(initial={
        'product': product,
        'source': 'PRODUCT',
        'message': f"Hello, I am interested in purchasing/inquiring about product: {product.name} (SKU: {product.sku}). Please provide pricing, stock availability, and bulk discount details."
    })

    context = {
        'product': product,
        'marketplace_links': marketplace_links,
        'related_products': related_products,
        'enquiry_form': enquiry_form,
    }
    return render(request, 'products/product_detail.html', context)


def marketplace_redirect_view(request, link_id):
    link = get_object_or_404(ProductMarketplaceLink, id=link_id, is_active=True)
    
    # Log analytics click
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    MarketplaceClick.objects.create(
        product=link.product,
        marketplace=link.marketplace,
        ip_address=ip,
        user_agent=user_agent
    )

    return redirect(link.url)


def product_search_suggestions_view(request):
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'suggestions': []})

    products = Product.objects.filter(is_active=True).filter(
        Q(name__icontains=query) |
        Q(sku__icontains=query) |
        Q(brand__name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(description__icontains=query) |
        Q(short_description__icontains=query) |
        Q(specifications__specification_name__icontains=query) |
        Q(specifications__specification_value__icontains=query)
    ).select_related('category', 'brand').prefetch_related('images').distinct()[:8]

    suggestions = []
    for p in products:
        primary_img = p.primary_image
        img_url = primary_img.image.url if (primary_img and primary_img.image) else ''
        suggestions.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'sku': p.sku,
            'category': p.category.name if p.category else '',
            'brand': p.brand.name if p.brand else '',
            'price': f"₹{p.current_price:.2f}",
            'image': img_url,
            'url': f"/products/{p.slug}/"
        })

    return JsonResponse({'suggestions': suggestions})
