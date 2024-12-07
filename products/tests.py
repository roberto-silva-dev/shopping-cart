from django.test import TestCase
from products.models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=100.0)

    def test_product_creation(self):
        """Test if the product is created correctly."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 100.0)

    def test_product_str(self):
        """Test the __str__ method of the Product model."""
        self.assertEqual(str(self.product), 'Test Product')
