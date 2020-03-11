from rest_framework import routers, serializers, viewsets

from project.models import CustomUser, RecognizedObject


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['fio', 'username', 'is_staff']


class RecognationObjectSerializer(serializers.ModelSerializer):

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
