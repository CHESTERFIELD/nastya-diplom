from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from rest_framework import viewsets

from project.api.v1.serializers import CustomUserSerializer
from project.models import RecognizedObject, CustomUser


def get_home_page(request):
    return render(request, 'base.html')


class RecognationObjectListView(ListView):
    model = RecognizedObject

    paginate_by = 10
    paginate_orphans = 4

    def get_queryset(self):
        if self.request.GET.get('from') and self.request.GET.get('to'):
            from_date = self.request.GET.get('from')
            to = self.request.GET.get('to')
            print(from_date, to)
            return RecognizedObject.objects.filter(created_datetime__gte=from_date, created_datetime__lte=to)
        return RecognizedObject.objects.filter(created_datetime__lte=timezone.now())


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
