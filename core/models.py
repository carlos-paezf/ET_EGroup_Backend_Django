from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import uuid
import os


def product_image_file_path(instance, filename):
    """ Generar el file path para la imagen del producto """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipes/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """ Crear y guardar un nuevo usuario """
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Crear superuser """
        super_user = self.create_user(email, password)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)

        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de Usuario que soporta hacer Login con Email en vez de username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def _str_(self):
        return self.name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Product(models.Model):
    """ Modelo para productos """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    title = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=500)
    slug = models.SlugField(unique=True)
    stock = models.IntegerField()
    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    image = models.ImageField(
        upload_to=product_image_file_path, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
