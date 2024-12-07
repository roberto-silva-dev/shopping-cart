from rest_framework import serializers
from cart.models import CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartItem
        fields = ['id', 'name', 'price', 'quantity']


class CartItemSerializerIn(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product_id', 'cart', 'quantity']
