"""culinary_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/xml')),
    path('sellers.json', TemplateView.as_view(template_name='sellers.json', content_type='text/json')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ushefa_admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('contact.urls', namespace='profile')),
    path('posts/', include('culinary_post.urls', namespace='culinary_post')),
    path('private/chat/', include('private_chat.urls', namespace='private_chat')),
    path('', include('culinary_recipe.urls', namespace='culinary_recipe')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)