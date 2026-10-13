from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('users/', user_list),
    path('users/<int:pk>/', user_detail),
    path('users/most-active/', most_active_users),
    path('users/statistics/', user_statistics),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
