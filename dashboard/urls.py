from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('registration.urls')),
    path('', views.dasboard, name='dashboard'),
    path('dashboard_orders', views.dasboardOrders, name='dashboard_orders'),
    path('list_message', views.dasboardMessage, name='list_message'),
    path('invoice<slug:invoice>/', views.invoiceView, name='invoice'),
    path('message<slug:message>/', views.messageView, name='message'),
    path('dashboard_amount', views.dasboardAmount, name='dashboard_amount'),
    path('view_donation', views.viewDonation, name='view_donation'),
]
