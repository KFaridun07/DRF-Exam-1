from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count,Q,Sum,Avg,Max,Min
from .models import *
from .serializers import (UserSerializer,ProfileSerializer,ProfileListSerializer,PostListSerializer,PostDetailSerializer,PostSerializer,
)




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



@api_view(['GET', 'POST'])
def profile_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.annotate(
            posts_count=Count('user__post', distinct=True)
        )

        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except Profile.DoesNotExist:
        return Response({'error': 'Профиль не найден'}, status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=204)


@api_view(['GET'])
def city_statistics(request):
    statistics = Profile.objects.values('city').annotate(profiles_count=Count('id')).order_by('-profiles_count')

    return Response(statistics)




@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.annotate(
            likes_count=Count('like', distinct=True),
            favorites_count=Count('favorite', distinct=True)
        )

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(
            {'error': 'Публикация не найдена'},
            status=404
        )

    if request.method == 'GET':
        post = Post.objects.annotate(
            likes_count=Count('like', distinct=True),
            favorites_count=Count('favorite', distinct=True)
        ).get(id=pk)

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)


@api_view(['GET'])
def user_posts(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(
            {'error': 'Пользователь не найден'},
            status=404
        )

    posts = Post.objects.filter(user=user).annotate(
        likes_count=Count('like', distinct=True),
        favorites_count=Count('favorite', distinct=True)
    )

    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def popular_posts(request):
    posts = Post.objects.annotate(
        likes_count=Count('like', distinct=True),
        favorites_count=Count('favorite', distinct=True)).filter(likes_count__gte=10).order_by('-likes_count')

    serializer = PostListSerializer(posts, many=True)

    data = []

    for post in serializer.data:
        data.append({'id': post['id'],'title': post['title'],'likes_count': post['likes_count'],'favorites_count': post['favorites_count'],'is_popular': post['is_popular']})

    return Response(data)


@api_view(['GET'])
def search_posts(request):
    q = request.GET.get('q')

    posts = Post.objects.annotate(
        likes_count=Count('like', distinct=True),
        favorites_count=Count('favorite', distinct=True)
    )

    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def filter_posts(request):
    min_views = request.GET.get('min_views')
    max_views = request.GET.get('max_views')
    user_id = request.GET.get('user_id')

    posts = Post.objects.annotate(
        likes_count=Count('like', distinct=True),
        favorites_count=Count('favorite', distinct=True)
    )

    if min_views:
        posts = posts.filter(views__gte=min_views)

    if max_views:
        posts = posts.filter(views__lte=max_views)

    if user_id:
        posts = posts.filter(user_id=user_id)

    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def post_statistics(request):
    statistics = Post.objects.aggregate(
        total_posts=Count('id'),
        total_views=Sum('views'),
        average_views=Avg('views'),
        max_views=Max('views'),
        min_views=Min('views')
    )

    statistics['total_likes'] = Like.objects.count()
    statistics['total_favorites'] = Favorite.objects.count()

    statistics['total_views'] = statistics['total_views'] or 0

    if statistics['average_views'] is not None:
        statistics['average_views'] = round(
            statistics['average_views'], 2
        )
    else:
        statistics['average_views'] = 0

    statistics['max_views'] = statistics['max_views'] or 0
    statistics['min_views'] = statistics['min_views'] or 0

    return Response(statistics)



@api_view(['GET'])
def author_statistics(request):
    authors = User.objects.annotate(
        posts_count=Count('post', distinct=True),
        total_views=Sum('post__views'),
        average_views=Avg('post__views'),
        likes_received=Count('post__like', distinct=True)
    )

    data = []

    for author in authors:
        data.append({
            'user_id': author.id,
            'username': author.username,
            'posts_count': author.posts_count,
            'total_views': author.total_views or 0,
            'average_views': round(author.average_views, 2)
                if author.average_views is not None else 0,
            'likes_received': author.likes_received
        })

    return Response(data)