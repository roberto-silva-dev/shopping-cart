from django.test import TestCase
from products.models import Product
from cart.models import Cart, CartItem
from users.models import CustomUser


class CartModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation_with_user(self):
        """Test if the cart is created correctly with a user."""
        self.assertEqual(self.cart.user, self.user)

    def test_cart_creation_without_user(self):
        """Test if the cart can be created without a user (using session_key)."""
        cart_without_user = Cart.objects.create(session_key='session123')
        self.assertEqual(cart_without_user.session_key, 'session123')

    def test_cart_str_with_user(self):
        """Test the __str__ method of the Cart model with a user."""
        self.assertEqual(str(self.cart), f"{self.user}'s cart")

    def test_cart_str_without_user(self):
        """Test the __str__ method of the Cart model without a user (using session_key)."""
        cart_without_user = Cart.objects.create(session_key='session123')
        self.assertEqual(str(cart_without_user), "session123's cart")


class CartItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=100.0)
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_creation(self):
        """Test if the cart item is created correctly."""
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_str(self):
        """Test the __str__ method of the CartItem model."""
        self.assertEqual(str(self.cart_item), 'Test Product (2x)')

    def test_cart_item_unique_constraint(self):
        """Test the unique constraint on cart and product in CartItem."""
        # Try to add another item with the same cart and product, should raise an error
        with self.assertRaises(Exception):
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
