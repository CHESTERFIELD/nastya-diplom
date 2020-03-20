from django.contrib.auth.decorators import login_required
from django.urls import path
from project.api.v1 import views
from project.api.v1.views import Pdf


urlpatterns = [
    path('home/', login_required(views.get_home_page, login_url='login'), name='home_page_url'),
    path('recognized-object/', login_required(views.RecognationObjectListView.as_view(), login_url='login'),
         name='rec_objs_list_url'),
    path('pdf/', login_required(Pdf.as_view(), login_url='login'), name='download_pdf'),
    path('register/', views.MyRegisterFormView.as_view(), name='register'),
]

