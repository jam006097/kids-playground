from __future__ import annotations
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from typing import Any, cast
import datetime


class CustomUserManager(BaseUserManager):
    """
    メールアドレスをユーザー名として扱うカスタムユーザーマネージャー。
    """

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "CustomUser":
        """ユーザーを作成する。"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = cast("CustomUser", self.model(email=email, **extra_fields))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "CustomUser":
        """スーパーユーザーを作成する。"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    メールアドレスを認証の主キーとするカスタムユーザーモデル。
    """

    email: str = models.EmailField("email address", unique=True)  # type: ignore
    account_name: str = models.CharField("アカウント名", max_length=50, default="名無し")  # type: ignore
    is_staff: bool = models.BooleanField("staff status", default=False)  # type: ignore
    is_active: bool = models.BooleanField("active", default=True)  # type: ignore
    date_joined: datetime.datetime = models.DateTimeField("date joined", default=timezone.now)  # type: ignore

    objects: CustomUserManager = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
