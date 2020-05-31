from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *


urlpatterns = [
    path('home/', login_required(get_home_page, login_url='login'), name='home_page_url'),
    path('recognized-object/', login_required(RecognationObjectListView.as_view(), login_url='login'),
         name='rec_objs_list_url'),
    path('pdf/', login_required(Pdf.as_view(), login_url='login'), name='download_pdf'),
    path('register/', MyRegisterFormView.as_view(), name='register'),
]

