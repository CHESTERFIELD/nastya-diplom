from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from project.models import CustomUser, RecognizedObject


class CustomUserSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [BasicAuthentication]

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])  # it hashed data
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['id', 'fio', 'username', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}


class RecognationObjectSerializer(serializers.ModelSerializer):
    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = RecognizedObject
        fields = ['user', 'created_datetime', 'user_photo']


class RecognationObjectFilteredSerializer(serializers.ModelSerializer):
    from_date = serializers.CharField()
    to = serializers.CharField()

    class Meta:
        model = RecognizedObject
        fields = ["from_date", "to"]

    def save(self, **kwargs):
        from_date = self.validated_data['from_date']
        to = self.validated_data['to']
        result = RecognizedObject.objects.filter(created_datetime__gte=from_date, created_datetime__lte=to)
        return result
