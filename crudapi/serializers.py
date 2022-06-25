from pkg_resources import require
from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    usertype = serializers.ChoiceField(required=True, choices=(('creator','creator'),('reader','reader')))
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'usertype')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username=validated_data['username']
        email = validated_data['email']
        password=validated_data['password']
        user = User.objects.create_user(username,email,password )
        if validated_data['usertype']=='creator':
            Creator.objects.create(username=user, name=user.username)
        elif validated_data['usertype']=='reader':
            Reader.objects.create(username=user, name=user.username)
            
        return user