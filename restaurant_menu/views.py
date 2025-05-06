from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
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
            item = get_object_or_404(Item, pk=item_id)
            item.quantity = quantity
            item.subtotal = item.price * quantity
            total += item.subtotal
            items.append(item)

        context['items'] = items
        context['total'] = total
        return context


def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')