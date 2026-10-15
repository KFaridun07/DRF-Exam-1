from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



