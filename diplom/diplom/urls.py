from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('project.api.urls')),
    path('project/', include('project.urls')),
    path('', views.get_redirect_to_home),
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = 'diplom.views.page_403'
handler404 = 'diplom.views.page_404'
handler500 = 'diplom.views.page_500'
