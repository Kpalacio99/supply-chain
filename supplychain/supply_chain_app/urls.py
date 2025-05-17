from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_goods, name='search_goods'),
    path('edit/<int:pk>/', views.edit_good, name='edit_good'),
    path('delete/<int:pk>/', views.delete_good, name='delete_good'),
    path('categories/', views.category_list, name='category_list'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('goods/', views.goods_list, name='goods_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/edit/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('barcode_scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('barcode_retrieve/', views.barcode_retrieve, name='barcode_retrieve'),
]