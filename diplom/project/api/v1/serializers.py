from rest_framework import serializers


from project.bl.util import generateAllDayForDate
from project.models import CustomUser, RecognizedObject


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])  # it hashed data
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['id', 'fio', 'username', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}


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
        to_date = generateAllDayForDate(to)
        result = RecognizedObject.objects.filter(created_datetime__gte=from_date, created_datetime__lte=to_date)
        return result


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def validate(self, data):
        return data


class PDFSerializer(serializers.Serializer):
    from_date = serializers.CharField()
    to = serializers.CharField()

    class Meta:
        fields = ["from_date", "to"]
        extra_kwargs = {
            'from_date': {'write_only': True},
            'to': {'write_only': True},
        }