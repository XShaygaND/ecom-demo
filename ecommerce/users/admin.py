from django.contrib import admin

from .models import User
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    list_display = (
        'id',
        'email',
        'is_seller',
        'is_staff',
        'is_superuser'
    )

    list_filter = (
        'is_seller',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    search_fields = (
        'id',
        'email',
    )

    readonly_fields = ('purchases', 'date_joined', 'last_login')

    fieldsets = [
        (
            None,
            {
                'fields': ['email', 'purchases', 'date_joined'],
            },
        ),
        (
            'stats',
            {
                "classes": ["collapse"],
                'fields': ['is_superuser', 'is_staff', 'is_active', 'is_seller', 'last_login']
            }
        )
    ]

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'is_seller', 'is_staff', 'is_superuser')
            }
        ),
    )
