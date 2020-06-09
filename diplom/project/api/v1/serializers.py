from rest_framework import serializers


from project.bl.util import generateAllDayForDate
from project.models import CustomUser, RecognizedObject
from project.utils_helper import prn


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


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'fio', 'username', 'is_staff', 'is_superuser']


class RecognationObjectSerializer(serializers.ModelSerializer):
    user_expand = serializers.SerializerMethodField()
    user = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = RecognizedObject
        fields = ['user_expand', 'user', 'created_datetime', 'user_photo']

    def get_user_expand(self, obj):
        serializer = CustomUserSerializer(instance=obj.user, read_only=True, context=self.context)
        return serializer.data

    def create(self, validated_data):
        prn(validated_data['user'])
        if validated_data['user'] != '':
            user = CustomUser.objects.get(username=validated_data['user'])
            validated_data['user'] = user
        else:
            validated_data['user'] = None
        
        prn(validated_data['user'])
        return RecognizedObject.objects.create(**validated_data)


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
    from_date = serializers.CharField(required=False, write_only=True)
    to = serializers.CharField(required=False, write_only=True)

    class Meta:
        fields = ["from_date", "to"]

    def validate(self, data):
        new_data = {}
        if data:
            new_data['from_date'] = data['from_date']
            new_data['to'] = generateAllDayForDate(data['to'])
        return new_data