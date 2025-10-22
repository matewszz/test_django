from django.contrib import admin
from .models import User, Crianca
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('id', 'first_name', 'last_name', 'username', 'email',
                    'is_staff')
    search_fields = ('id', 'first_name', 'username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),

        (('Status'), {'fields': ('status',)}),
        (('permissao'), {'fields': ('permissao',)})

    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',
                       'first_name', 'last_name', 'is_staff', 'is_active'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('id',)


@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    ...