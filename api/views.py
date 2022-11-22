# from django.shortcuts import render
# from rest_framework import generics,permissions
# from rest_framework.response import Response
# from knox.models import AuthToken
# from .serializers import *

# from django.contrib.auth import login
# from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.views import LoginView as KnoxLoginView

# # Create your views here.


# # Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user":UserSerializer(user, context=self.get_serializer_context()).data,
#             "token":AuthToken.objects.create(user)[1]
#         })


# # Login API
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)



# 2
# from rest_framework import generics,permissions,mixins
# from rest_framework.response import Response
# from .serializers import *
# from django.contrib.auth.models import User


# # Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user":UserSerializer(user,context=self.get_serializer_context()).data,
#             "message":"User Created Successfully.",
#         })


# 3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import *
from .serializers import *
import jwt, datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.parsers import JSONParser


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = [serializer.data]
            return Response({
                "status":True,
                "status_code":status.HTTP_200_OK,
                "discription":"login success",
                "data": data,
            })
        return Response(serializer.errors)


class LoginView(APIView):
    def post(self, request):
        serializer_data = JSONParser().parse(request)
        serializer = LoginSerializer(data=serializer_data)
        password = serializer_data['password']
        user_name = serializer_data['user_name']
        try:

            if serializer.is_valid(raise_exception=True):
                if '@' in user_name:
                    id = Register.objects.filter(email_id=user_name,password=password).first()
                else:
                    id = Register.objects.filter(user_name=user_name,password=password).first()
                user_id = id.user_id
                payload = {
                    'id': user_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')
                
                # token.decode('utf-8')

                response = Response()

                response.set_cookie(key='jwt', value=token, httponly=True)
                print("adffdsafaf",response)
                response.data = {
                    'status':True,
                    'status_code':status.HTTP_200_OK,
                    'description':'login success',
                    'data':[{
                        "user_id":user_id
                        }] 
                }
                return response
            return Response(serializer.errors)
        except Exception as e:
            print(e)


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        print("asdfghjkhgfds",token)

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = RegisterSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response