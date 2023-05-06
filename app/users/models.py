from typing import Optional

from academic_plans.models import AcademicPlan, EducationalProgram, FieldOfStudy
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Model manager for User model with no username field
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user: AbstractUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model
    """

    USERNAME_FIELD = "email"

    username = None

    first_name = models.CharField("Имя", max_length=150)

    middle_name = models.CharField("Отчество", max_length=150, blank=True)

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")

    objects = UserManager()

    educational_program: Optional[EducationalProgram] = models.ForeignKey(
        to="academic_plans.EducationalProgram",
        on_delete=models.SET_NULL,
        related_name="users",
        blank=True,
        null=True,
        verbose_name="Образовательная программа",
    )

    field_of_study: Optional[FieldOfStudy] = models.ForeignKey(
        to="academic_plans.FieldOfStudy",
        on_delete=models.SET_NULL,
        related_name="users",
        blank=True,
        null=True,
        verbose_name="Направление подготовки",
    )

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "middle_name",
        "educational_program",
        "field_of_study",
    ]
