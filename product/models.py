from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
import uuid
import os


def product_image_file_path(instance, filename):
    """ Generar el file path para la imagen del producto """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipes/', filename)


class Product(models.Model):
    """ Modelo para productos """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    title = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[
        MinValueValidator(0)
    ])
    description = models.TextField(max_length=500)
    slug = models.SlugField(max_length=255, unique=True)
    stock = models.IntegerField(default=0, validators=[
        MinValueValidator(0)
    ])
    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    rating = models.FloatField(default=3.5, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    image = models.ImageField(upload_to=product_image_file_path, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
