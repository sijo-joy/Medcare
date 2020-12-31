from django.urls import path, include

from . import views
urlpatterns = [
    path('', include('registration.urls')),
    path('', include('lend_and_returns.urls')),
    path('donation', views.donationPage, name='donation'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profilePage, name='profile'),
    path('add_cart', views.addToCart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('product_view/<int:product>/', views.viewProduct, name='view_product'),
    path('remove_from_cart/<int:cart_item>/', views.removeFromCart, name='remove_cart_item'),
    path('products', views.products, name='products'),
    path('products/<slug:category>/', views.products, name='products'),
    path('products/<slug:search>/', views.products, name='products'),
    path('products/<slug:sort>/', views.products, name='products'),
    path('products/<slug:category>/<slug:sort>', views.products, name='products'),
    path('products/<slug:page>/<slug:sort>', views.products, name='products'),
    path('products/<slug:category>/<slug:sort>/<slug:page>', views.products, name='products'),
]
