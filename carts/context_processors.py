from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            """
                if User is authenticated then take 
                the count based on the users
            """
            if request.user.is_authenticated:
                cart_item = CartItem.objects.all().filter(user=request.user)
            else:
                cart_item = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_item:
                cart_count += cart_item.quantity
        except Cart.DoesNotExists:
            cart_count = 0
    return dict(cart_count=cart_count)
