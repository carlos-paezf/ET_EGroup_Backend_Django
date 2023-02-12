from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Product
from product.serializers import ProductSerializer
import tempfile
import os
from PIL import Image


PRODUCT_URL = reverse('product:product-list')


def image_upload_url(product_id):
    """ Devuelve la URL para subir una imagen de un producto """
    return reverse('product:product-upload-image', args=[product_id])


def detail_url(product_id):
    """ Devuelve la URL de detalle de un producto """
    return reverse('product:product-detail', args=[product_id])


def sample_product(user, **params):
    """ Crear un producto de ejemplo """
    defaults = {
        "title": "Nuevo producto4",
        "price": 12.99,
        "description": "Descripción del nuevo producto",
        "slug": "nuevo-producto-4",
        "stock": 10,
        "tags": ["Tag 1", "Tag 2"]
    }
    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ Pruebas de la API de recetas públicas """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ > Probar que se requiere iniciar sesión para acceder a la API """
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductViewSetTestCase(TestCase):
    """ > Probar la API de productos """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.valid_payload = {
            'name': 'Test Product Updated',
        }
        self.invalid_payload = {
            'name': '',
        }

    def test_list_product(self):
        """ > Listar los productos """
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_product(self):
        """ > Crear un producto con payload valido  """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/product/', data=sample_product, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        """ > Intentar crear un producto invalido """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/product/', data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_product(self):
        """ > Devolver un producto buscado """
        response = self.client.get(f'/product/{self.product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_valid_product(self):
        """ > Actualizar todo el contenido de un producto """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            f'/product/{self.product.pk}/', data=sample_product, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_product(self):
        """ > Intentar actualizar un producto invalido """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            f'/product/{self.product.pk}/', data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_product(self):
        """ > Actulizar parcialmente un elemento """
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f'/product/{self.product.pk}/', data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.valid_payload['name'])
