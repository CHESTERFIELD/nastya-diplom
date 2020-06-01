import jwt
from django.contrib.auth import login, logout, user_logged_in
from rest_framework import viewsets, mixins, views, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.serializers import jwt_payload_handler

from diplom import settings
from project.api.v1.serializers import CustomUserSerializer, RecognationObjectSerializer, \
    RecognationObjectFilteredSerializer, UserLoginSerializer, PDFSerializer
from project.bl.util import generateAllDayForDate
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
            if user.is_active:
                login(request, user)

            return Response(new_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     username = request.data['username']
        #     password = request.data['password']
        #
        #     user = CustomUser.objects.get(username=username, password=password)
        #     if user:
        #         try:
        #             payload = jwt_payload_handler(user)
        #             token = jwt.encode(payload, settings.SECRET_KEY)
        #             user_details = {}
        #             user_details['name'] = "%s %s" % (
        #                 user.first_name, user.last_name)
        #             user_details['token'] = token
        #             user_logged_in.send(sender=user.__class__,
        #                                 request=request, user=user)
        #             return Response(user_details, status=status.HTTP_200_OK)
        #
        #         except Exception as e:
        #             raise e
        #     else:
        #         res = {
        #             'error': 'can not authenticate with the given credentials or the account has been deactivated'}
        #         return Response(res, status=status.HTTP_403_FORBIDDEN)
        # except KeyError:
        #     res = {'error': 'please provide a email and a password'}
        #     return Response(res)


class PdfAPIView(views.APIView):
    serializer_class = PDFSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        serializer = PDFSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            from_date = new_data['from_date']
            to = new_data['to']
            to_date = generateAllDayForDate(to)
            rec_objects = RecognizedObject.objects.filter(created_datetime__gte=from_date,
                                                          created_datetime__lte=to_date)
        else:
            rec_objects = RecognizedObject.objects.all()
        params = {
            'rec_objects': rec_objects,
            'request': request,
            'static': settings.STATIC_ROOT
        }
        return Render.render('project/pdf.html', params)
