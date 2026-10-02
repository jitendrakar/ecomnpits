from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Case, When, Value, IntegerField
from django.core.paginator import Paginator
from .models import Product, ProductCategory, Brand, ProductMarketplaceLink, MarketplaceClick
from enquiries.forms import EnquiryForm


STOP_WORDS = {'the', 'a', 'an', 'for', 'with', 'in', 'and', 'or', 'of', 'to', 'is', 'at', 'by', 'on', 'it', 'this', 'that'}


def get_search_words(query_str):
    raw_words = query_str.strip().split()
    words = [w for w in raw_words if len(w) > 1 and w.lower() not in STOP_WORDS]
    if not words:
        words = [w for w in raw_words if len(w) > 0]
    return words


def build_single_word_q(word):
    return (
        Q(name__icontains=word) |
        Q(sku__icontains=word) |
        Q(brand__name__icontains=word) |
        Q(category__name__icontains=word) |
        Q(description__icontains=word) |
        Q(short_description__icontains=word) |
        Q(specifications__specification_name__icontains=word) |
        Q(specifications__specification_value__icontains=word)
    )


def search_products_smart(base_qs, query_str, limit=None):
    query_str = query_str.strip()
    if not query_str:
        return base_qs

    words = get_search_words(query_str)
    if not words:
        return base_qs.none()

    # 1. Try EXACT Full Phrase match
    exact_q = build_single_word_q(query_str)
    exact_pks = list(base_qs.filter(exact_q).values_list('pk', flat=True).distinct())

    # 2. Try ALL words match (AND query)
    all_words_q = Q()
    for word in words:
        all_words_q &= build_single_word_q(word)
    all_words_pks = list(base_qs.filter(all_words_q).values_list('pk', flat=True).distinct())

    # 3. Try ANY word match (OR query for multi-word 4-5 word queries)
    any_words_q = Q()
    for word in words:
        any_words_q |= build_single_word_q(word)
    any_words_pks = list(base_qs.filter(any_words_q).values_list('pk', flat=True).distinct())

    # Combine PKs in order of relevance (exact phrase > all words > any related words)
    seen = set()
    ordered_pks = []

    for pk in exact_pks + all_words_pks + any_words_pks:
        if pk not in seen:
            seen.add(pk)
            ordered_pks.append(pk)

    if limit and len(ordered_pks) > limit:
        ordered_pks = ordered_pks[:limit]

    if not ordered_pks:
        return base_qs.none()

    # Preserve exact relevance order safely across database engines
    whens = [When(pk=pk, then=Value(i)) for i, pk in enumerate(ordered_pks)]
    return base_qs.filter(pk__in=ordered_pks).annotate(
        relevance_rank=Case(*whens, output_field=IntegerField())
    ).order_by('relevance_rank')


def product_list_view(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images', 'marketplace_links')

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    brand_slug = request.GET.get('brand', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    warranty = request.GET.get('warranty', '').strip()
    stock = request.GET.get('stock', '').strip()
    sort = request.GET.get('sort', '').strip()

    has_query = bool(query)
    if query:
        products = search_products_smart(products, query)

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
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif not has_query:
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

    base_qs = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images')
    products = search_products_smart(base_qs, query, limit=8)

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
