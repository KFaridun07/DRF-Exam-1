
from rest_framework import serializers
from .models import User, Profile, Post, Like, Favorite



class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    posts_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','full_name','age','posts_count','likes_count','favorites_count']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'





class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'city', 'birth_date', 'avatar']


class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id','user','bio','city','birth_date','avatar','posts_count',]

    def get_user(self, obj):
        return {'id': obj.user.id,'username': obj.user.username}



class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)
    is_popular = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title','content','author','views','created_at','updated_at','likes_count','favorites_count','is_popular']

    def get_author(self, obj):
        return {'id': obj.user.id,'username': obj.user.username}

    def get_is_popular(self, obj):
        return obj.likes_count >= 10


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)
    liked_by = serializers.SerializerMethodField()
    favorited_by = serializers.SerializerMethodField()
    is_popular = serializers.SerializerMethodField()
    is_viral = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title','content','author','views','likes_count','favorites_count','liked_by','favorited_by','is_popular','is_viral','status',]

    def get_author(self, obj):
        return {'id': obj.user.id,'username': obj.user.username}

    def get_liked_by(self, obj):
        users = User.objects.filter(like__post=obj).distinct()
        return [{'id': user.id, 'username': user.username}for user in users]

    def get_favorited_by(self, obj):
        users = User.objects.filter(favorite__post=obj).distinct()
        return [{'id': user.id, 'username': user.username}for user in users]

    def get_is_popular(self, obj):
        return obj.likes_count >= 10

    def get_is_viral(self, obj):
        return obj.views >= 1000

    def get_status(self, obj):
        if obj.likes_count > 0:
            return 'has_likes'
        return 'no_likes'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user','title','content','views','created_at','updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

    def get_user(self, obj):
        return {'id': obj.user.id,'username': obj.user.username}

    def get_post(self, obj):
        return {'id': obj.post.id,'title': obj.post.title}