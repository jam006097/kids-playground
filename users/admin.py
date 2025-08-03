from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "is_staff", "is_active"]

    # ユーザー編集画面のフィールド
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # ユーザー追加画面のフィールド
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2"),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)

    # UserAdminが参照するusernameをなくす
    USERNAME_FIELD = "email"

    # UserAdminのget_fieldsetsをオーバーライドしてusernameを排除
    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets

    # UserAdminのget_add_fieldsetsをオーバーライドしてusernameを排除
    def get_add_fieldsets(self, request, obj=None):
        return self.add_fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
