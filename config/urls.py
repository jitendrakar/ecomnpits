from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom admin titles
admin.site.site_header = "NEHRU PLACE IT SERVICES ADMIN PANEL"
admin.site.site_title = "Nehru Place IT Services Administration"
admin.site.index_title = "Platform Management Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('services/', include('services.urls')),
    path('enquiries/', include('enquiries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
handler403 = 'core.views.handler403'
