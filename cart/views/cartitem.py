from django.db import IntegrityError
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from cart.utils import get_cart
from cart.models import CartItem
from cart.serializers import CartItemSerializerIn, CartItemSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


class CartItemAPIView(generics.GenericAPIView):
    http_method_names = ['post', 'options']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartItemSerializer
        return CartItemSerializerIn

    def get_queryset(self):
        filters = {}
        if self.request.GET.get('name') is not None:
            filters['product__name__icontains'] = self.request.GET.get('name')
        return CartItem.objects.select_related('cart', 'product').filter(cart__user=self.request.user, **filters)

    def get_object(self, pk=None):
        try:
            return CartItem.objects.select_related('product', 'cart').get(id=pk)
        except CartItem.DoesNotExist:
            raise Http404

    def _get_object_as_dict(self, pk):
        return CartItemSerializer(self.get_object(pk)).data

    @extend_schema(
        request=CartItemSerializerIn,
        responses={
            200: CartItemSerializer,
            400: OpenApiResponse(description="Bad Request: Validation error or other issue"),
        },
        description="Adds an item to the shopping cart or updates the quantity if it already exists.",
        summary="Add (or upgrade quantity) cart item",
    )
    def post(self, request, *args, **kwargs):
        try:
            cart = get_cart(self.request)
            if not cart:
                return Response({"message": "Cart not found"}, status=status.HTTP_400_BAD_REQUEST)
            data = self.request.data.copy()
            instance = CartItem.objects.filter(cart=cart, product_id=data.get('product_id')).first()
            if instance and (isinstance(data.get('quantity', 1), int) or data.get('quantity', 1).isdigit()):
                data['quantity'] = instance.quantity + int(data.get('quantity', 1))
            serializer = self.get_serializer(instance, data=data, partial=True if instance else False)
            itemcard = serializer.is_valid() and serializer.save(cart=cart)
            if itemcard:
                return Response(self._get_object_as_dict(itemcard.pk), status=status.HTTP_200_OK)
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(e)
            return Response({"message": "Something went wrong on database."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)


class CartItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete', 'options']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartItemSerializer
        return CartItemSerializerIn

    def get_queryset(self):
        return CartItem.objects.select_related('cart', 'product').filter(
            **(
                {'cart__user': self.request.user} if self.request.user.is_authenticated
                else {'cart__session_key': self.request.session.session_key}
            )
        )

    def _get_object_as_dict(self):
        return CartItemSerializer(self.get_object()).data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self._get_object_as_dict(), status=status.HTTP_200_OK)

    @extend_schema(
        request=CartItemSerializerIn,
        responses={
            200: CartItemSerializer,
            400: OpenApiResponse(description="Bad Request: Validation error or other issue"),
        },
        description="Updates an item in the shopping cart.",
        summary="Update cart item",
    )
    def patch(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(
        description="Remove an item in the shopping cart.",
        summary="Remove cart item",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(self, request, *args, **kwargs)

    @extend_schema(
        responses={
            200: CartItemSerializer,
        },
        description="Retrieve an item in the shopping cart.",
        summary="Get cart item",
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


