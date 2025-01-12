from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.test import TestCase
from datetime import timedelta

from django.core.exceptions import ValidationError

from products.models import Product
from users.models import User
from .models import Seller


class SellerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com', password='Pass123', is_seller=True)
        Seller.objects.create(
            name="Test Seller",
            description="Test Seller Description",
            owner=self.user,
        )

    def test_seller_default_fields(self):
        seller = Seller.objects.get(name="Test Seller")
        current_time = now()

        self.assertEqual(seller.name, "Test Seller")
        self.assertEqual(seller.description, "Test Seller Description")
        self.assertEqual(seller.owner, self.user)
        self.assertAlmostEqual(seller.join_date, current_time, delta=timedelta(seconds=1))
        self.assertEqual(seller.sales, 0)
        self.assertEqual(seller.slug, slugify(seller.name).lower())
        self.assertEqual(seller.is_active, True)

    def test_seller_can_have_multiple_products(self):
        seller = Seller.objects.get(name="Test Seller")
        prod1 = Product.objects.create(
            name="Product 1",
            description="Product Description 1",
            price=1.99,
            seller=seller,
        )
        prod2 = Product.objects.create(
            name="Product 2",
            description="Product Description 2",
            price=2.99,
            seller=seller,
        )

        self.assertEqual(seller.products.count(), 2)

    def test_seller_join_date_doesnt_change_on_update(self):
        seller = Seller.objects.get(name="Test Seller")

        original_join_date = seller.join_date
        seller.sales += 1
        seller.save()

        seller = Seller.objects.get(name="Test Seller")

        self.assertEqual(seller.join_date, original_join_date)

    def test_seller_sales_increment(self):
        seller = Seller.objects.get(name="Test Seller")
        seller.sales += 1
        seller.save()

        self.assertEqual(seller.sales, 1)

    def test_seller_sales_not_negative(self):
        seller = Seller.objects.get(name="Test Seller")
        seller.sales = -1

        self.assertRaises(ValidationError, seller.save)

    def test_seller_str(self):
        seller = Seller.objects.get(name="Test Seller")

        self.assertEqual(str(seller), "Test Seller")

    def test_seller_bool(self):
        seller = Seller.objects.get(name="Test Seller")

        self.assertEqual(bool(seller), seller.is_active)

    def test_seller_owner_is_seller(self):
        user = User.objects.create(email='test2@email.com', password='Pass123')
        seller = Seller.objects.get(name="Test Seller")

        seller.owner = user

        self.assertRaises(ValueError, seller.save)

