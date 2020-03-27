from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, FormView
from django.views.generic.base import View
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from diplom import settings
from project.api.v1.serializers import CustomUserSerializer, RecognationObjectSerializer, \
    RecognationObjectFilteredSerializer
from project.forms import CustomUserCreationForm
from project.models import RecognizedObject, CustomUser
from project.render import Render
from project.utils_helper import prn


def get_home_page(request):
    return render(request, 'project/home.html')


class RecognationObjectViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = RecognizedObject.objects.all()
    serializer_class = RecognationObjectSerializer
    permission_classes = []
    
    def get_queryset(self):
        return super().get_queryset().filter(created_datetime__lte=timezone.now())

    @action(methods=["GET"], detail=False, serializer_class=RecognationObjectFilteredSerializer,
            url_name='get-filter-recognitation-objects-set', url_path='filter-rec-obj-set')
    def get_calen_set(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        serializer_result = RecognationObjectSerializer(result, many=True)
        return Response(serializer_result.data)


class CustomUserViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = ()


class RecognationObjectListView(ListView):
    model = RecognizedObject

    paginate_by = 10
    paginate_orphans = 4

    def get_queryset(self):
        if self.request.GET.get('from') and self.request.GET.get('to'):
            from_date = self.request.GET.get('from')
            to = self.request.GET.get('to')
            print(from_date, to)
            return RecognizedObject.objects.filter(created_datetime__gte=from_date, created_datetime__lte=to).\
                order_by('-created_datetime')
        return RecognizedObject.objects.filter(created_datetime__lte=timezone.now()).order_by('-created_datetime')

    def get_context_data(self, **kwargs):
        context = super(RecognationObjectListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем ее некоторым значением
        first_date_created_object = RecognizedObject.objects.filter(created_datetime__lte=timezone.now()).\
                            order_by('created_datetime').first()
        first_day_date = first_date_created_object.created_datetime.strftime("%Y-%m-%d")
        last_date_created_object = RecognizedObject.objects.filter(created_datetime__lte=timezone.now()). \
            order_by('-created_datetime').first()
        last_day_date = last_date_created_object.created_datetime.strftime("%Y-%m-%d")
        context['from'] = first_day_date
        context['to'] = last_day_date
        return context


class Pdf(LoginRequiredMixin, View):

    def get(self, request):
        if self.request.GET.get('from') and self.request.GET.get('to'):
            from_date = self.request.GET.get('from')
            to = self.request.GET.get('to')
            rec_objects = RecognizedObject.objects.filter(created_datetime__gte=from_date, created_datetime__lte=to).\
                order_by('-created_datetime')
            prn(rec_objects)
        else:
            rec_objects = RecognizedObject.objects.filter(created_datetime__lte=timezone.now()).\
                order_by('-created_datetime')
            prn(rec_objects)
        params = {
            'rec_objects': rec_objects,
            'request': request,
            'static': settings.STATIC_ROOT
        }
        return Render.render('project/pdf.html', params)


class MyRegisterFormView(FormView):
    # Указажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
    # это UserCreationForm - стандартный класс Django унаследованный
    form_class = CustomUserCreationForm
    success_url = "/home/"
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)
