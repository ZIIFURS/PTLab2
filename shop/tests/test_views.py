from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product_in_stock = Product.objects.create(
            name="Бриллиантовое колье Tiffany",
            price=12000000,
            quantity=2
        )
        self.product_out_of_stock = Product.objects.create(
            name="Яхта Azimut 100 Leonardo",
            price=850000000,
            quantity=0
        )

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_status_and_content(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tiffany")
        self.assertContains(response, "2 шт.")
        self.assertContains(response, "Нет в наличии")

    def test_buy_page_accessible_when_in_stock(self):
        response = self.client.get(reverse('buy', args=[self.product_in_stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введите свое имя")
        self.assertContains(response, "Введите адрес доставки")

    def test_successful_purchase_decreases_quantity(self):
        initial_quantity = self.product_in_stock.quantity
        response = self.client.post(reverse('buy', args=[self.product_in_stock.id]), {
            'person': 'Екатерина Великая',
            'address': 'Зимний дворец, Санкт-Петербург'
        }, follow=True)

        self.assertContains(response, "Спасибо за покупку")
        self.assertContains(response, "Екатерина Великая")

        self.product_in_stock.refresh_from_db()
        self.assertEqual(self.product_in_stock.quantity, initial_quantity - 1)

        self.assertTrue(Purchase.objects.filter(
            person="Екатерина Великая",
            product=self.product_in_stock
        ).exists())

    def test_cannot_buy_when_out_of_stock_via_post(self):
        response = self.client.post(reverse('buy', args=[self.product_out_of_stock.id]), {
            'person': 'Тест',
            'address': 'Тест'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Purchase.objects.filter(product=self.product_out_of_stock).exists())
