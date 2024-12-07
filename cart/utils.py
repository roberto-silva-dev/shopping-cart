from cart.models import Cart
from core.settings import VIP_PERCENT_DISCOUNT


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def calculate_total(request, cart):
    ret = 0, 0, 0
    if not cart or not isinstance(cart, Cart):
        return ret
    items = cart.items.all()
    if not len(items):
        return ret
    total_sum = sum(item.product.price * item.quantity for item in items)
    total = calculate_get_3_for_2(items, total_sum)
    if request.user.is_authenticated and (cart.user.user_type or 'common') == 'vip':
        total = min(total, calculate_vip_discount(items))
    return round(total_sum, 2), round(total, 2), round(total_sum-total, 2)


def calculate_get_3_for_2(cart_items, total):
    items = []
    for item in cart_items:
        items.extend([item.product] * item.quantity)
    items.sort(key=lambda p: p.price)
    discount = items[0].price if len(items) >= 3 else 0
    return total - discount


def calculate_vip_discount(cart_items=None, total=None):
    cart_items = cart_items or []
    if not total:
        return sum(item.product.price * item.quantity for item in cart_items) * (100 - VIP_PERCENT_DISCOUNT) / 100
    return total * (100 - VIP_PERCENT_DISCOUNT) / 100


