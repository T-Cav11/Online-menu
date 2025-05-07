from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.MenuList.as_view(), name='home'),
    path('item/<int:pk>',views.MenuItemDetail.as_view(), name="menu_item"),
    path('item/cart/',views.view_cart, name="view_cart"),
    path('about/',views.AboutPage.as_view(), name="about"),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.CheckoutPage.as_view(), name='checkout'),


]