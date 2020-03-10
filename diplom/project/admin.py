from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'fio', 'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('username', 'fio', 'is_staff', 'is_active', 'last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'fio', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'fio', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserPhoto)
admin.site.register(RecognizedObject)
