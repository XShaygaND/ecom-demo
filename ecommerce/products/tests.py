from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta

from users.models import User
from sellers.models import Seller
from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(email='test@email.com', password='Pass123', is_seller=True)
        self.seller = Seller.objects.create(
            name="Test Seller",
            description="Test Seller Description",
            owner=user
        )
        Product.objects.create(
            name="Test Product",
            seller=self.seller,
            description="Test Description",
            price=10.99,
        )

    def test_product_default_fields(self):
        product = Product.objects.get(name="Test Product")
        current_time = now()

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Description")
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.seller, self.seller)
        self.assertEqual(product.sales, 0)
        self.assertEqual(product.stock, 0)
        self.assertAlmostEqual(product.sub_date, current_time, delta=timedelta(seconds=1))
        self.assertEqual(product.is_active, True)

    def test_product_price_not_zero(self):
        product = Product.objects.get(name="Test Product")
        product.price = 0

        self.assertRaises(ValidationError, product.save)

    def test_product_price_not_negative(self):
        product = Product.objects.get(name="Test Product")
        product.price = -1

        self.assertRaises(ValidationError, product.save)

    def test_product_sub_date_doesnt_change_on_update(self):
        product = Product.objects.get(name="Test Product")

        original_sub_date = product.sub_date
        product.price = 20.99
        product.save()

        product = Product.objects.get(name="Test Product")

        self.assertEqual(product.sub_date, original_sub_date)

    def test_product_sales_not_negative(self):
        product = Product.objects.get(name="Test Product")
        product.sales = -1

        self.assertRaises(ValidationError, product.save)

    def test_product_stock_not_negative(self):
        product = Product.objects.get(name="Test Product")
        product.stock = -1

        self.assertRaises(ValidationError, product.save)

    def test_product_str(self):
        product = Product.objects.get(name="Test Product")

        self.assertEqual(str(product), "Test Product")

    def test_product_bool(self):
        product = Product.objects.get(name="Test Product")

        self.assertTrue(bool(product), True)
