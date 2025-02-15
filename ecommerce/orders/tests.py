from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from decimal import Decimal

from .models import Order
from carts.models import Cart, CartItem
from products.models import Product
from sellers.models import Seller


user = get_user_model()

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = user.objects.create(email='test@email.com', password='Pass123')
        self.suser = user.objects.create(email='test2@email.com', password='Pass123', is_seller=True)
        seller = Seller.objects.create(
            name='Test Seller',
            description='Test Seller Description',
            owner=self.suser,
        )
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=20.99,
            seller=seller,
        )
        CartItem.objects.create(
            cart=Cart.objects.get(owner=self.user),
            product = product,
            quantity=1,
        )

    def test_order_default_fields(self):
        cart = Cart.objects.get(owner=self.user)
        order = Order.objects.create(cart=cart, total_sum=cart.total_sum)

        self.assertTrue(order.is_active)
        self.assertEqual(order.total_sum, Decimal('20.99'))
        self.assertEqual(order.cart, cart)
        self.assertFalse(order.after_pay)
        self.assertEqual(order.status, Order.Status.PENDING)
        
    def test_order_empty_cart(self):
        scart = Cart.objects.get(owner=self.suser)

        with self.assertRaises(ValidationError):
            Order.objects.create(cart=scart, total_sum=scart.total_sum)

    def test_order_wrong_total_sum(self):
        cart = Cart.objects.get(owner=self.user)
        order = Order.objects.create(cart=cart, total_sum=cart.total_sum + 2)

        self.assertEqual(order.total_sum, cart.total_sum)

    def test_order_auto_cart_deactivation(self):
        cart = Cart.objects.get(owner=self.user)
        Order.objects.create(cart=cart, total_sum=cart.total_sum)

        self.assertFalse(cart.is_active)

    def test_order_inactive_modification(self):
        cart = Cart.objects.get(owner=self.user)
        order = Order.objects.create(cart=cart, total_sum=cart.total_sum)

        order.is_active = False
        order.save()

        with self.assertRaises(ValidationError):
            order.status = Order.Status.DELIVERED
            order.save()
            order.full_clean()
            print(order.status)
