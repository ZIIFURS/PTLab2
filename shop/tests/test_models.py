from django.core.exceptions import ValidationError
from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Золотые часы Patek Philippe",
            price=25_000_000,
            quantity=5
        )

    def test_product_has_quantity_field(self):
        self.assertEqual(self.product.quantity, 5)

    def test_can_be_purchased_returns_true_when_quantity_gt_0(self):
        self.assertTrue(self.product.can_be_purchased())

    def test_can_be_purchased_returns_false_when_quantity_0(self):
        self.product.quantity = 0
        self.product.save()
        self.assertFalse(self.product.can_be_purchased())

    def test_decrease_quantity_success(self):
        self.product.decrease_quantity()
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 4)

    def test_decrease_quantity_raises_error_when_zero(self):
        self.product.quantity = 0
        self.product.save()
        with self.assertRaises(ValidationError):
            self.product.decrease_quantity()

    def test_str_method(self):
        self.assertIn("Patek Philippe", str(self.product))
        self.assertIn("5 шт.", str(self.product))


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price="740")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov",
                                address="Svetlaya St.")

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))