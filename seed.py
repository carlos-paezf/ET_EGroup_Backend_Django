from django.contrib.auth import get_user_model
from django.core.files import File
from django_seed import Seed
import random
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from product.models import Product

User = get_user_model()


def create_product(product_seeder):
    user = User.objects.order_by("?").first()
    product = product_seeder.faker.word()
    price = product_seeder.faker.random_number(digits=2)
    description = product_seeder.faker.sentence()
    stock = product_seeder.faker.random_number(digits=2)
    image = Image.new("RGB", size=(200, 200), color=(73, 109, 137))
    file_obj = BytesIO()
    image.save(file_obj, format="JPEG")
    file_obj.seek(0)
    django_file = File(file_obj, name=f"{product}.jpeg")
    product_seeder.add_entity(
        Product,
        user=user,
        title=product,
        price=price,
        description=description,
        stock=stock,
        image=django_file
    )


seeder = Seed.seeder()
seeder.add_entity(User, 10)
seeder.add_entity(Product, number=100, seed_func=create_product)
inserted_pks = seeder.execute()
