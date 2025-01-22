from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Cart, CartItem
from products.models import Product
from sellers.models import Seller


user = get_user_model()

class CartTestCase(TestCase):
    def setUp(self):
        self.user = user.objects.create(email='test@email.com', password='Pass123')

    def test_cart_auto_creation_on_user_creation(self):
        self.assertTrue(Cart.objects.filter(owner=self.user).exists())

    def test_cart_default_fields(self):
        cart = Cart.objects.get(owner=self.user)

        self.assertEqual(cart.count, 0)
        self.assertTrue(cart.is_active)

    def test_cart_count_not_negative(self):
        cart = Cart.objects.get(owner=self.user)

        cart.count = -1

        self.assertRaises(ValidationError, cart.save)

    def test_cart_only_one_for_user(self):
        cart = Cart.objects.get(owner=self.user)

        with self.assertRaises(ValidationError):
            Cart.objects.create(owner=self.user)

    def test_cart_few_carts_for_seller(self):
        suser = user.objects.create(email='test2@email.com', password='Pass123', is_seller=True)

        Cart.objects.create(owner=suser)

        self.assertEqual(suser.carts.count(), 2)


class CartCountTestCase(TestCase):
    def setUp(self):
        self.user = user.objects.create(email='test@email.com', password='Pass123')
        self.suser = user.objects.create(email='test2@email.com', password='Pass123', is_seller=True)
        seller = Seller.objects.create(
            name='Test Seller',
            description='Test Seller Description',
            owner=self.suser,
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=20.99,
            seller=seller,
        )
        self.cart = Cart.objects.get(owner=self.user)

    def test_cart_count_single_item(self):
        CartItem.objects.create(cart=self.cart, product=self.product)

        self.assertEqual(self.cart.count, 1)

    def test_cart_count_single_item_multiple_quantity(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        self.assertEqual(self.cart.count, 2)

    def test_cart_count_increment_by_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product)
        cart_item.quantity += 1
        cart_item.save()

        self.assertEqual(self.cart.count, 2)

    def test_cart_count_multiple_items_different(self):
        _suser = user.objects.create(email='test3@email.com', password='Pass123', is_seller=True)
        _seller = Seller.objects.create(
            name='Test Seller2',
            description='Test Seller Description',
            owner=self.suser,
        )
        _product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=20.99,
            seller=_seller,
        )
        CartItem.objects.create(cart=self.cart, product=self.product)
        CartItem.objects.create(cart=self.cart, product=_product)

        self.assertEqual(self.cart.count, 2)

    def test_cart_count_multiple_items_duplicate(self):
        CartItem.objects.create(cart=self.cart, product=self.product)
        CartItem.objects.create(cart=self.cart, product=self.product)

        self.assertEqual(self.cart.count, 2)


class CartItemTestCase(TestCase):
    def setUp(self):
        self.user = user.objects.create(email='test@email.com', password='Pass123')
        self.suser = user.objects.create(email='test2@email.com', password='Pass123', is_seller=True)
        seller = Seller.objects.create(
            name='Test Seller',
            description='Test Seller Description',
            owner=self.suser,
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=20.99,
            seller=seller,
        )
        self.cart = Cart.objects.get(owner=self.user)
        CartItem.objects.create(cart=self.cart, product=self.product)

    def test_cart_item_default_fields(self):
        cartitem = CartItem.objects.get(cart=self.cart)

        self.assertEqual(cartitem.cart, self.cart)
        self.assertEqual(cartitem.product, self.product)
        self.assertEqual(cartitem.quantity, 1)

    def test_cart_item_quantity_not_negative(self):
        cartitem = CartItem.objects.get(cart=self.cart)

        cartitem.quantity = -1

        self.assertRaises(ValidationError, cartitem.save)

    def test_cart_item_quantity_increment(self):
        cartitem = CartItem.objects.get(cart=self.cart)

        cartitem.quantity += 1
        cartitem.save()

        self.assertEqual(cartitem.quantity, 2)

    def test_cart_item_add_with_multiple_quantity(self):
        cart = Cart.objects.get(owner=self.suser)
        cartitem = CartItem.objects.create(cart=cart, product=self.product, quantity=3)


        self.assertEqual(cart.cartitems.all()[0].quantity, 3)

    def test_cart_duplicate_item_merging(self):
        cart = self.cart
        cartitem = CartItem.objects.get(cart=cart)

        CartItem.objects.create(cart=cart, product=self.product)

        self.assertEqual(cart.cartitems.all()[0].quantity, 2)
        self.assertEqual(cart.cartitems.all().count(), 1)

    def test_cart_item_add_to_seller_cart(self):
        scart = Cart.objects.get(owner=self.suser)
        cartitem = CartItem.objects.create(cart=scart, product=self.product)

        self.assertTrue(self.suser.carts.exists())
        self.assertEqual(self.suser.carts.all()[0].cartitems.all()[0], cartitem)

    def test_cart_item_in_multiple_carts(self):
        cart = Cart.objects.get(owner=self.user)
        cartitem = CartItem.objects.get(cart=self.cart)

        scart = Cart.objects.get(owner=self.suser)
        CartItem.objects.create(cart=scart, product=self.product)

        self.assertTrue(cartitem.product == scart.cartitems.get(product=self.product).product)

