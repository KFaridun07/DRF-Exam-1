
from rest_framework import serializers
from .models import User, Profile, Post, Like, Favorite


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    posts_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','full_name','age','posts_count','likes_count','favorites_count',]

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'