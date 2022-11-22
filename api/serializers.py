# from rest_framework import serializers
# from django.contrib.auth.models import User


# # User serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','email')


# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','email','password',)
#         extra_kwargs = {
#             'password':{'write_only':True}
#         }
#         def create(self,validated_data):
#             user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
#             return user

# 2
# from os import umask
# from rest_framework import serializers
# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password


# # Register serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','password','first_name','last_name')
#         extra_kwargs = {
#             'password':{'write_only':True},
#         }

#         def create(self,validate_data):
#             user = User.objects.create_user(
#             validate_data['username'],
#             password = validate_data['password'],
#             first_name = validate_data['first_name'],
#             last_name = validate_data['last_name'])
           
#             return user


# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from .models import *
from django.db.models import Q



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['user_id','user_name', 'password', 'email_id','phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, attrs):
        queryset = Register.objects.filter(Q(user_name=attrs['user_name']) | Q(email_id=attrs['email_id']))
        if queryset:
            raise serializers.ValidationError(
                {"message": "Username or email already exists."})
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['user_name', 'password']
    def validate(self, attrs):
        user_name = attrs['user_name']
        password = attrs['password']
        
        if '@' in user_name:
            username_exist = Register.objects.filter(email_id=user_name).exists()
        else:
            username_exist = Register.objects.filter(user_name=user_name).exists()

        password_exist = Register.objects.filter(password=password).exists()
     
        if not username_exist:
            raise serializers.ValidationError({"message":"User not found!"})
        if not password_exist:
            raise serializers.ValidationError({"message":"Incorrect password!"})
        return attrs