from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from pyexpat.errors import messages
from django.contrib import messages

from .models import Item, MEAL_TYPE
from django.views.generic import TemplateView

class MenuList(generic.ListView):
    queryset = Item.objects.order_by("date_created")
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meals"] = MEAL_TYPE

        return context


class MenuItemDetail(generic.DetailView):
    model = Item
    template_name = "menu_item_detail.html"


class AboutPage(TemplateView):
    template_name = "about.html"

class CheckoutPage(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        items = []
        total = 0



        for item_id, quantity in cart.items():
            try:
                item = get_object_or_404(Item, pk=item_id)
                item.quantity = quantity
                item.subtotal = item.price * quantity
                total += item.subtotal
                items.append(item)
            except:
                # if the item no longer exists, remove it from the cart
                del cart[item_id]
                self.request.session.modified = True

        context['items'] = items
        context['total'] = total
        return context


def add_to_cart(request, item_id):
    # Ensure session is initialized
    if 'cart' not in request.session:
        request.session['cart'] = {}

    # Convert item_id to string since session keys must be strings
    item_id_str = str(item_id)

    # Get current cart or initialize empty dictionary
    cart = request.session.get('cart', {})

    # Add item to cart or increment quantity
    cart[item_id_str] = cart.get(item_id_str, 0) + 1

    # Save cart back to session
    request.session['cart'] = cart

    # Mark session as modified to ensure it gets saved
    request.session.modified = True

    # Add success message
    item = get_object_or_404(Item, pk=item_id)
    messages.success(request,f"{item} added to your cart")

    return redirect('view_cart')


def view_cart(request):
    # Get the cart from the session
    cart = request.session.get('cart', {})
    items = []
    total = 0

    # Process each item in the cart
    for item_id, quantity in cart.items():
        try:
            item = get_object_or_404(Item, pk=item_id)
            item.quantity = quantity
            item.subtotal = item.price * quantity
            total += item.subtotal
            items.append(item)
        except:
            # If item doesn't exist anymore, remove it
            del cart[item_id]
            request.session.modified = True

    context = {
        'items': items,
        'total': total
    }

    return render(request, 'cart.html', context)


def update_cart(request, item_id):
    # Get the cart from the session
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)

    # If the item exists in the cart, update its quantity
    if item_id_str in cart:
        # Get the new quantity from the request
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[item_id_str] = quantity
        else:
            # Remove the item if quantity is 0 or negative
            del cart[item_id_str]

    # Save cart back to session
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    # Get the cart from the session
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)

    # Remove the item if it exists in the cart
    if item_id_str in cart:
        del cart[item_id_str]

    # Save cart back to session
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


def clear_cart(request):
    # Clear the cart in the session
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True

    return redirect('view_cart')