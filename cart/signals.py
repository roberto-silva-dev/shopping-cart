from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from cart.models import Cart, CartItem


@receiver(user_logged_in)
def migrate_cart_to_user(sender, request, user, **kwargs):
    user_cart = Cart.objects.filter(user=user).first() or None
    session_key = getattr(request, 'original_session_key', None)
    try:
        if session_key:
            cart = Cart.objects.get(session_key=session_key)
            if user_cart:
                new_items = {}
                for item in (user_cart.items.all() | cart.items.all()):
                    if item.product_id in new_items:
                        new_items[item.product_id].quantity += item.quantity
                    else:
                        new_items[item.product_id] = CartItem(
                            product=item.product,
                            quantity=item.quantity,
                        )
                    new_items[item.product_id].cart = user_cart

                with transaction.atomic():
                    user_cart.items.all().delete()
                    CartItem.objects.bulk_create(
                        list(new_items.values()),
                        update_conflicts=True,
                        unique_fields=['cart', 'product'],
                        update_fields=['quantity'],
                    )
                    cart.items.all().delete()
                    cart.delete()
                    print(f'Cart {cart.pk} from session {session_key} migrated to cart {user_cart.pk} from user {user}')
            elif cart:
                cart.user = user
                cart.session_key = None
                cart.save()
                print(f'Cart {cart.pk} passed from session {session_key} to user {user}')
    except Cart.DoesNotExist:
        pass
