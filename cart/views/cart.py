from rest_framework import generics
from rest_framework.response import Response
from cart.utils import get_cart, calculate_total
from cart.serializers import CartItemSerializer


class CartAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        items, items_sum, total, discount = [], 0, 0, 0
        if self.request.session.session_key or self.request.user.is_authenticated:
            cart = get_cart(self.request)
            items_sum, total, discount = calculate_total(self.request, cart)
            items = CartItemSerializer(cart.items.all(), many=True).data
        return Response({
            'sum': items_sum,
            'discount': discount,
            'total': total,
            'items': items
        })
