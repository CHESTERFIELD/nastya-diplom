from django.conf.urls import handler404
from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework import routers
from project.api.v1 import views

router = routers.SimpleRouter()
router.register(r'v1/users', views.CustomUserViewSet, basename='')
router.register(r'v1/recognitation-objects', views.RecognationObjectViewSet, basename='recog_objects')

urlpatterns = [
]

urlpatterns += router.urls

