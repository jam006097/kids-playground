from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import CustomUser

# デフォルトのUserモデルが登録されている場合、解除する
# これにより、カスタムUserモデルの管理画面が正しく表示されるようになる
try:
    admin.site.unregister(get_user_model())
except admin.sites.NotRegistered:
    pass

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # 管理画面での表示項目をCustomUserモデルに合わせて調整
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    # ユーザー追加/変更フォームのフィールドセットをCustomUserモデルに合わせて調整
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_confirm'),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)