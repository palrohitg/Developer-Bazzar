from django.shortcuts import render
from store.models import Product


def home(request):
    """
        filter return the queryset and looping each elements
        will give the counts of the objects
        - single projects can't be iterated
        - single objects is present in the code then directly pass those values
    """
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'home.html', context)
