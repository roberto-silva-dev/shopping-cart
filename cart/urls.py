from django.urls import path
from cart.views.cartitem import *
from cart.views.cart import *

urlpatterns = [
    path('', CartAPIView.as_view()),
    path('items', CartItemAPIView.as_view()),
    path('items/<int:pk>', CartItemRetrieveUpdateDestroyAPIView.as_view()),
]
