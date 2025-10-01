"""
URL configuration for dailyvotion_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from django.templatetags.static import static
from django.conf import settings
from django.conf.urls.static import static as django_static
from pages import views as pages
from django.conf import settings
from django.conf.urls.static import static as django_static

urlpatterns = [
    # Redirect legacy favicon.ico requests to our SVG favicon
    path('favicon.ico', RedirectView.as_view(url=static('favicon.svg'), permanent=True)),
    path('admin/', admin.site.urls),
    path('', pages.home, name='home'),
    path('about/', pages.about, name='about'),
    path('login/', pages.login_view, name='login'),
    path('register/', pages.register, name='register'),
    path('profile/', pages.profile, name='profile'),
    path('logout/', pages.logout_view, name='logout'),
    path('journal/', pages.journal, name='journal'),
    path('journalentries/', pages.journalentries, name='journalentries'),
    path('editprofile/', pages.edit_profile, name='edit_profile'),
    path('userprayerrequest/', pages.user_prayer_request, name='user_prayer_request'),
    path('userreflection/', pages.user_reflection, name='user_reflection'),
    path('userfeedback/', pages.user_feedback, name='user_feedback'),
    path('adminlogin/', pages.admin_login, name='admin_login'),
    path('adminregister/', pages.admin_register, name='admin_register'),
    path('adminauth/', pages.admin_auth, name='admin_auth'),
    path('admindashboard/', pages.admin_dashboard, name='admin_dashboard'),
    path('managecontent/', pages.manage_content, name='manage_content'),
    path('managefeedback/', pages.manage_feedback, name='manage_feedback'),
    path('manageuser/', pages.manage_user, name='manage_user'),
    path('manageprayer/', pages.manage_prayer, name='manage_prayer'),
    path('manageprayerhistory/', pages.manage_prayer_history, name='manage_prayer_history'),
    # Health check
    path('gallery/', pages.gallery, name='gallery'),
    path('healthz', pages.healthz, name='healthz'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += django_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add a pattern for media files in production (WhiteNoise will handle these)
if not settings.DEBUG and settings.MEDIA_URL.startswith('/static/'):
    pass  # No need to add patterns - WhiteNoise will serve from STATIC_ROOT
