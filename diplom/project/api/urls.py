from django.contrib.auth.decorators import login_required
from django.urls import path

from project.api.v1 import views

urlpatterns = [
    path('home/', login_required(views.get_home_page, login_url='login'), name='home_page_url'),
    path('recognized-object/', login_required(views.RecognationObjectListView.as_view(), login_url='login'),
         name='rec_objs_list_url'),
]

