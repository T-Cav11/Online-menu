from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.MenuList.as_view(), name='home'),
    path('item/<int:pk>',views.MenuItemDetail.as_view(), name="menu_item"),
    path('about/',views.AboutPage.as_view(), name="about"),
    path('checkout/',views.CheckoutPage.as_view(),name="checkout"),
    path('item/checkout/',views.CheckoutPage.as_view(),name="checkout")
]