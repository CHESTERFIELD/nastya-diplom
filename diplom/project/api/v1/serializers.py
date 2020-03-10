from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from project.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'is_staff']
