from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    path('', include('cars.urls')),
    
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
