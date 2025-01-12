from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta

from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test@email.com", password='pass123')

    def test_user_default_fields(self):
        user = User.objects.get(email="test@email.com")
        current_time = now()

        self.assertEqual(user.email, "test@email.com")
        self.assertAlmostEqual(user.date_joined, current_time, delta=timedelta(seconds=1))
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_seller, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.purchases, 0)

    def test_user_purchases_not_negative(self):
        user = User.objects.get(email="test@email.com")
        user.purchases = -1

        self.assertRaises(ValidationError, user.save)

    def test_user_purchases_increment(self):
        user = User.objects.get(email="test@email.com")
        user.purchases += 1
        user.save()

        self.assertEqual(user.purchases, 1)

    def test_user_join_date_doesnt_change_after_update(self):
        user = User.objects.get(email="test@email.com")

        original_join_date = user.date_joined
        user.purchases += 1
        user.save()

        self.assertEqual(user.date_joined, original_join_date)
