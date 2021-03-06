"""pdfa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'accTool.views.preview_pdf'),
    url(r'^upload/', 'accTool.views.upload_pdf'),
    url(r'^uploadprogress/', 'accTool.views.upload_progress'),
    url(r'^imagep/', 'accTool.views.image_preview'),
    # url(r'^imagealt/', 'accTool.views.image_alt'),
    url(r'^imagealtsubmit/$', 'accTool.views.image_alt_submit'), 
    url(r'^imagealtexport/$', 'accTool.views.image_alt_export'), 
    url(r'^headings/', 'accTool.views.heading_preview'),
    url(r'^metadata/$', 'accTool.views.metadata_preview'), 
    url(r'^login/$', 'accTool.views.user_login'), 
    url(r'^logout/$', 'accTool.views.user_logout', name='logout'), 
]

urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
