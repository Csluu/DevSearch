from django.contrib import admin
from django.urls import path, include

# these two imports are for images
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    # sends the user to projects.urls 
    path('projects/', include('projects.urls')),
    path('', include('users.urls'))
    
]

# for images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# for production 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)