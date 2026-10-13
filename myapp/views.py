from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import *
from .serializers import UserSerializer,ProfileSerializer




@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.annotate(
            posts_count=Count('post', distinct=True),
            likes_count=Count('like', distinct=True),
            favorites_count=Count('favorite', distinct=True)
        )

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=404)

    if request.method == 'GET':
        user = User.objects.annotate(posts_count=Count('post', distinct=True),likes_count=Count('like', distinct=True),favorites_count=Count('favorite', distinct=True)
        ).get(id=pk)

        serializer = UserSerializer(user)
        data = serializer.data

        try:
            profile = Profile.objects.get(user=user)
            data['profile'] = ProfileSerializer(profile).data
        except Profile.DoesNotExist:
            data['profile'] = None

        return Response(data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=204)


@api_view(['GET'])
def most_active_users(request):
    users = User.objects.annotate(
        posts_count=Count('post', distinct=True)).order_by('-posts_count')[:10]

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_statistics(request):
    from django.db.models import Avg, Min, Max

    statistics = User.objects.aggregate(
        total_users=Count('id'),
        average_age=Avg('age'),
        min_age=Min('age'),
        max_age=Max('age')
    )

    if statistics['average_age'] is not None:
        statistics['average_age'] = round(statistics['average_age'], 2)

    return Response(statistics)