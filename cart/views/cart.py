from rest_framework import generics
from rest_framework.response import Response
from cart.utils import get_cart, calculate_total
from cart.serializers import CartSerializerOut
from drf_spectacular.utils import extend_schema


class CartAPIView(generics.GenericAPIView):
    @extend_schema(
        responses={
            200: CartSerializerOut,
        },
        description="Retrieve the cart details",
        summary="Get cart details",
    )
    def get(self, request, *args, **kwargs):
        items, items_sum, total, discount = [], 0, 0, 0
        if self.request.session.session_key or self.request.user.is_authenticated:
            cart = get_cart(self.request)
            items_sum, total, discount = calculate_total(self.request, cart)
            items = cart.items.all()
        return Response(CartSerializerOut({
            'sum': items_sum,
            'discount': discount,
            'total': total,
            'items': items
        }).data)
