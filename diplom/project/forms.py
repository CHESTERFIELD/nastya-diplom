from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from diplom import settings
from project.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'fio', 'is_staff', 'is_active')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)
