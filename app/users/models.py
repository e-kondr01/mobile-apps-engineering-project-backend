from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class StudyGroup(models.Model):

    code = models.CharField(max_length=31, verbose_name="Код группы")

    program_name = models.CharField(max_length=255, verbose_name="Название направления")

    enrollment_year = models.PositiveSmallIntegerField(
        verbose_name="Год начала обучения"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активна?")

    class EducationLevels(models.IntegerChoices):
        BACHELOR = 0, "Бакалавриат"
        MASTER = 1, "Магистратура"
        PHD = 2, "Аспирантура"

    education_level = models.PositiveSmallIntegerField(
        choices=EducationLevels.choices,
        default=EducationLevels.BACHELOR,
        verbose_name="Уровень образования",
    )

    def __str__(self) -> str:
        return self.program_name + " " + str(self.enrollment_year)

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"


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
    Custom user model with required email and no username
    """

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    username = None

    first_name = None

    last_name = None

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")

    objects = UserManager()

    study_group: StudyGroup | None = models.ForeignKey(
        to=StudyGroup,
        on_delete=models.SET_NULL,
        related_name="users",
        blank=True,
        null=True,
        verbose_name="Учебная группа",
    )
