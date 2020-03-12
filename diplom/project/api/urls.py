from django.conf.urls import handler404
from django.contrib.auth.decorators import login_required
from django.urls import path
from rest_framework import routers
from project.api.v1 import views
from project.api.v1.views import Pdf

router = routers.SimpleRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'recognitation-objects', views.RecognationObjectViewSet, basename='recog_objects')

urlpatterns = [
    path('home/', login_required(views.get_home_page, login_url='login'), name='home_page_url'),
    path('recognized-object/', login_required(views.RecognationObjectListView.as_view(), login_url='login'),
         name='rec_objs_list_url'),
    path('pdf/', Pdf.as_view())
]

urlpatterns += router.urls

