from django.conf.urls import url
from rest_framework import routers
from project.api.v1 import views

router = routers.SimpleRouter()

router.register(r'v1/users', views.CustomUserViewSet, basename='all_users')
router.register(r'v1/recognition-objects', views.RecognationObjectViewSet, basename='recognition_objects')

urlpatterns = [
    url(r'v1/login/', views.LoginAPIView.as_view(), name='login'),
    url(r'v1/logout/', views.LogoutAPIView.as_view(), name='logout'),
    url(r'v1/download-pdf/', views.PdfAPIView.as_view(), name='download-pdf'),
]

urlpatterns += router.urls

