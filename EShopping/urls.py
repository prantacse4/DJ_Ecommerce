from django.contrib import admin
from django.urls import path,re_path, include
from django.conf import settings
from django.conf.urls.static import static
# from Shop import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Ecom.urls')),
    path('', include('Product.urls')),
    path('', include('Order.urls')),
    path('', include('accounts.urls')),
    # path('', include('accounts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# wrongurls = [
#     re_path('.*/', views.wrong, name='wrong'),
# ]
# urlpatterns += wrongurls