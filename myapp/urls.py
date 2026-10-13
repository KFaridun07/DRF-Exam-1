from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('users/', user_list),
    path('users/<int:pk>/', user_detail),
    path('users/most-active/', most_active_users),
    path('users/statistics/', user_statistics),
    path('profiles/', profile_list),
    path('profiles/<int:pk>/', profile_detail),
    path('profiles/city-statistics/', city_statistics),
    path('posts/', post_list),
    path('posts/<int:pk>/', post_detail),
    path('users/<int:pk>/posts/', user_posts),
    path('posts/popular/', popular_posts),
    path('posts/search/', search_posts),
    path('posts/filter/', filter_posts),
    path('posts/statistics/', post_statistics),
    path('posts/author-statistics/', author_statistics),
    path('likes/', like_list),
    path('likes/<int:pk>/', like_detail),
    path('posts/<int:pk>/likes/', post_likes),
    path('likes/top-posts/', top_posts_by_likes),
    path('favorites/', favorite_list),
    path('favorites/<int:pk>/', favorite_detail),
    path('users/<int:pk>/favorites/', user_favorites),
    path('users/<int:pk>/analytics/', user_analytics),
    path('dashboard/', dashboard),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
