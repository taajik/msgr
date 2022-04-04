
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = ("email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "date_joined", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
