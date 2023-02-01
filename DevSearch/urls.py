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
    path('', include('users.urls'))
    
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    
]

# for images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# for production 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)