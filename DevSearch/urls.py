from django.contrib import admin
from django.urls import path, include

# these two imports are for images
from django.conf import settings
from django.conf.urls.static import static 

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # sends the user to projects.urls 
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),
    
    # Have to keep it like this for password reset for django

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name="password_reset_complete"),
    
]

# for images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# for production 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)