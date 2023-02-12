from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email="test@mail.com", password="test_123"):
    """ Crear usuario de ejemplo """
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """ > Probar la creación de un usuario con un email de manera correcta """
        email = "test@gmail.com"
        password = "test_123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ > Probar que el correo de un nuevo usuario está normalizado """
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, '123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ > Probar error de creación de usuario con email invalido """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_super_user(self):
        """ > Probar super-usuario creado """
        user = get_user_model().objects.create_superuser(
            'admin@gmail.com', 'admin_1234567890')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_product_str(self):
        """ > Probar representación en cadena de texto del producto """
        product = models.Product.objects.create(
            user=sample_user(),
            title="Laptop",
            price=5.00,
            description="lorem ipsum",
            slug='laptop',
            stock=2
        )

        self.assertEqual(str(product), product.title)

    @patch('uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """ > Probar que el nombre del archivo del producto es un UUID """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipes/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
