from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from core.settings import STATIC_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('cart/', include('cart.urls')),
    path('', include('core.urls_docs')),

    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
