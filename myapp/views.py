from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import User
from .serializers import UserSerializer



@api_view(['GET'])
def user_list(request):
    users = User.objects.annotate(
        posts_count=Count('post', distinct=True),
        likes_count=Count('like', distinct=True),
        favorites_count=Count('favorite', distinct=True)
    )

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

