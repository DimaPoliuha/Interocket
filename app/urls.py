from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', base_view, name='base'),
    path('tour/<slug:tour_slug>/', tour_view, name='tour_detail'),
    path('category/<slug:category_slug>/', category_view, name='category_detail'),
    path('add-to-cart/', add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/', cart_view, name='cart'),
    path('order/', order_view, name='order'),
    path('checkout/', checkout_view, name='checkout'),
    path('account/', account_view, name='account'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='base'), name='logout'),

]
