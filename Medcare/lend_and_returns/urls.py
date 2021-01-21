from django.urls import path, include

from . import views
urlpatterns = [
    path('', include('registration.urls')),
    path('book', views.bookPay, name='book_pay'),
    path('order', views.viewOrder, name='order'),
    path('checkout', views.viewCheckout, name='check_out'),
    path('order/<slug:lend_order_id>/', views.viewOrder, name='order'),
]
