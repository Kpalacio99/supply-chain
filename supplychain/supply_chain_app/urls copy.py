from django.urls import path
from . import views  # Import views from the current module (app)

urlpatterns = [
    path('', views.home, name='home'),  # Home page of the site (redirects to home view)
    path('login/', views.login, name='login'),  # Login page (redirects to login view)
    path('signup/', views.signup, name='signup'),  # Signup page for new users (redirects to signup view)
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard after login (redirects to dashboard view)
    path('search/', views.search_goods, name='search_goods'),  # Search goods page (search functionality view)
    path('edit/<int:pk>/', views.edit_good, name='edit_good'),  # Edit goods (uses primary key of the good to edit)
    path('delete/<int:pk>/', views.delete_good, name='delete_good'),  # Delete goods (uses primary key to delete a good)
    path('categories/', views.category_list, name='category_list'),  # List of categories (category list view)
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),  # Delete category (uses primary key to delete)
    path('goods/', views.goods_list, name='goods_list'),  # List of goods (goods listing view)
    path('customers/', views.customer_list, name='customer_list'),  # List of customers (customer list view)
    path('customers/edit/<int:pk>/', views.edit_customer, name='edit_customer'),  # Edit customer details (uses primary key to edit)
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),  # Delete customer (uses primary key to delete)
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),  # Edit category (uses primary key to edit)
    path('barcode_scanner/', views.barcode_scanner, name='barcode_scanner'),  # Barcode scanner page (product entry via barcode)
    path('barcode_retrieve/', views.barcode_retrieve, name='barcode_retrieve'),  # Retrieve product by barcode
]
