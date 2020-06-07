import jwt
from django.contrib.auth import logout
from rest_framework import viewsets, mixins, views, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from diplom import settings
from project.api.v1.serializers import CustomUserSerializer, RecognationObjectSerializer, \
    RecognationObjectFilteredSerializer, UserLoginSerializer, PDFSerializer, CustomUserUpdateSerializer
from project.models import RecognizedObject, CustomUser
from project.render import Render
from project.utils_helper import prn


class RecognationObjectViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin):
    queryset = RecognizedObject.objects.all()
    serializer_class = RecognationObjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().all()

    @action(methods=["GET"], detail=False, serializer_class=RecognationObjectFilteredSerializer,
            url_name='filter_set', url_path='filter_set')
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
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.data['id'])
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class LoginAPIView(views.APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            user = CustomUser.objects.get(username=new_data['username'])
            if user.is_superuser:
                new_data['is_superuser'] = True

            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PdfAPIView(views.APIView):
    serializer_class = PDFSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        serializer = PDFSerializer(data=request.GET)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            if new_data:
                from_date = new_data['from_date']
                to = new_data['to']
                rec_objects = RecognizedObject.objects.filter(created_datetime__gte=from_date,
                                                              created_datetime__lte=to)
            else:
                rec_objects = RecognizedObject.objects.all()
        else:
            rec_objects = RecognizedObject.objects.all()
        params = {
            'rec_objects': rec_objects,
            'request': request,
            'static': settings.STATIC_ROOT
        }
        return Render.render('project/pdf.html', params)
