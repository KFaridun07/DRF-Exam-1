from rest_framework.serializers import ModelSerializer

from .models import CustomUser


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password']


    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )

        return user