from django.shortcuts import render, redirect, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # product_variation = []
    # if request.method == 'POST':
    #     for item in request.POST:
    #         key = item
    #         value = request.POST[key]

    #         try:
    #             variation = Variation.objects.get(product=product,
    #                                               variation_category__iexact=key, variation_value__iexact=value)
    #             product_variation.append(variation)
    #         except:
    #             pass

    try:
        """
        Creating Session id to add the product
        to Cart
        """
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    # try:
    #     cart_item = CartItem.objects.create(
    #         product=product, quantity=1, cart=cart)
    #     if len(product_variation) > 0:
    #         cart_item.variations.clear()
    #         for item in product_variation:
    #             cart_item.variations.add(item)
    #     cart_item.save()
    # except CartItem.DoesNotExists:
    #     cart_item = CartItem.objects.create(
    #         product=product,
    #         quantity=1,
    #         cart=cart,
    #     )

    #     if len(product_variation) > 0:
    #         cart_item.variations.clear()
    #         for item in product_variation:
    #             cart_item.variations.add(item)
    #     cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(
        Product, id=product_id)  # give 404 if not found
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    '''
     Delete the cart item when click on 
     remove button 
    '''
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        # if request.user.is_authenticated:
        #     cart_items = CartItem.objects.filter(
        #         user=request.user, is_active=True)
        # else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    """Cart pages will be shown"""
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    """Cart pages will be shown"""
    return render(request, 'store/checkout.html', context)
