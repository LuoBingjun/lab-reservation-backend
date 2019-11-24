from django.db import models

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib import auth

from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token

import time
import re
from uuid import uuid4

from api.models import User, UserGroup


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=5, max_length=30)
    password = serializers.CharField(min_length=5, max_length=50)
    email = serializers.RegexField(re.compile('.+@.*tsinghua.edu.cn', re.I))
    phone = serializers.DecimalField(max_digits=11, decimal_places=0)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']


class Register(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        info = RegisterSerializer(data=request.data)
        if info.is_valid():
            username = info.validated_data['username']
            password = info.validated_data['password']
            email = info.validated_data['email']
            phone = info.validated_data['phone']
            if User.objects.filter(username=username).exists():
                return Response('Username already exists', status=400)
            else:
                user = User.objects.create_user(
                    username=username, email=email, phone=phone, password=password)
                default_group = UserGroup.objects.get(name='default')
                user.groups.add(default_group)
                return Response(status=200)
        else:
            return Response(info.errors, status=400)


class LoginInfo(serializers.Serializer):
    username = serializers.CharField(min_length=5, max_length=30)
    password = serializers.CharField(min_length=5, max_length=50)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        info = LoginInfo(data=request.data)
        if info.is_valid():
            username = info.validated_data.get("username", "")
            password = info.validated_data.get("password", "")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.logout(request)
                auth.login(request, user)
                group = UserGroup.objects.get(user=user)
                response = Response({
                    'admin':user.is_staff,
                    'max_reserve':group.max_reserve
                })
                response['Set-Cookie'] = 'sessionid=' + \
                    request.session.session_key+';Path=/'
                return response
            else:
                return Response('Wrong username and password', status=400)
        else:
            return Response(info.errors, status=400)


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone']


class Setinfo(APIView):
    def post(self, request):
        info = InfoSerializer(data=request.data)
        if info.is_valid():
            user = request.user
            user.__dict__.update(info.validated_data)
            user.save()
            return Response(status=200)
        else:
            return Response(info.errors, status=400)


class PwdInfo(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=5, max_length=50)
    newpwd = serializers.CharField(min_length=5, max_length=50)


class Setpwd(APIView):
    def post(self, request):
        info = PwdInfo(data=request.data)
        if info.is_valid():
            oldpwd = info.validated_data['oldpwd']
            newpwd = info.validated_data['newpwd']
            user = auth.authenticate(
                username=request.user.username, password=oldpwd)
            if user is not None:
                user.set_password(newpwd)
                user.save()
                auth.logout(request)
                return Response(status=200)
            else:
                return Response('Wrong old password', status=401)
        else:
            return Response(info.errors, status=400)


class Logout(APIView):
    def post(self, request):
        auth.logout(request)
        return Response(status=200)
