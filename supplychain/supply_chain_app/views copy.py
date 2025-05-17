
# Imports the render and redirect functions to display templates and handle redirects
from django.shortcuts import render, redirect

# Imports all models defined in the current app's models.py
from .models import *

# A decorator to restrict access to views unless the user is logged in
from django.contrib.auth.decorators import login_required

# Imports the authenticate and login functions to handle user login
from django.contrib.auth import authenticate, login as auth_login

# Imports all forms defined in the current app's forms.py
from .forms import *

# Helper function to fetch an object or return a 404 error if it doesn't exist
from django.shortcuts import get_object_or_404

# Used to build complex queries using OR, AND, NOT operators
from django.db.models import Q

# Imports Django’s built-in User model (used if you're not using a custom user model)
from django.contrib.auth.models import User



# def home(request):
#     return render(request, 'home.html')
# A simple view function to render the home page
def home(request):
    # Renders and returns the 'home.html' template when a user accesses the home URL
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Create the user with hashed password
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Log the user in right after signup
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

        return redirect("dashboard")

    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            return render(request, 'login.html', {"error": "Invalid credentials"})
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('q', '')  # Get the search query
    edit_mode = False
    good_instance = None

    goods = Goods.objects.filter(user=request.user).order_by('-date_added')  # Filter by logged-in user
    if query:
        goods = goods.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Check if we're editing a good
    if 'edit_good' in request.GET:
        edit_mode = True
        good_id = request.GET.get('edit_good')
        good_instance = get_object_or_404(Goods, id=good_id, user=request.user)  # Ensure the good belongs to the user
        goods_form = GoodsForm(request.POST or None, instance=good_instance)
    else:
        goods_form = GoodsForm(request.POST or None)

    category_form = CategoryForm(request.POST or None, prefix='category')
    customer_form = CustomerForm(request.POST or None)

    categories = Category.objects.filter(user=request.user)
    customers = Customer.objects.filter(user=request.user)  # Filter customers by the logged-in user

    if request.method == 'POST':
        if 'submit_good' in request.POST:
            if good_instance:
                goods_form = GoodsForm(request.POST, instance=good_instance)
            else:
                goods_form = GoodsForm(request.POST)

            if goods_form.is_valid():
                good = goods_form.save(commit=False)
                good.user = request.user  # Assign the logged-in user
                goods_form.save()
                return redirect('dashboard')

        elif 'submit_category' in request.POST and category_form.is_valid():
            category_form.save()
            return redirect('dashboard')

        elif 'submit_customer' in request.POST and customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.user = request.user  # Assign the logged-in user
            customer_form.save()
            return redirect('dashboard')

    context = {
        'form': goods_form,
        'category_form': category_form,
        'customer_form': customer_form,
        'goods': goods,
        'categories': categories,
        'customers': customers,
        'query': query,
        'edit_mode': edit_mode,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def customer_list(request):
    customers = Customer.objects.filter(user=request.user).order_by('-date_added')  # Filter customers by the logged-in user
    form = CustomerForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # Assign the logged-in user
            form.save()
            return redirect('customer_list')

    return render(request, 'customer_list.html', {
        'customers': customers,
        'form': form,
    })


@login_required(login_url='login')
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)  # Ensure the customer belongs to the user
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})


@login_required(login_url='login')
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)  # Ensure the customer belongs to the user
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return redirect('customer_list')



@login_required(login_url='login')
def edit_good(request, pk):
    # Ensure the good belongs to the logged-in user
    good = get_object_or_404(Goods, pk=pk, user=request.user)
    
    # Initialize the form with the existing good instance
    form = GoodsForm(request.POST or None, instance=good)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')

    # Fetch only categories and customers that belong to the logged-in user
    categories = Category.objects.filter(user=request.user)
    customers = Customer.objects.filter(user=request.user)

    context = {
        'form': form,
        'categories': categories,
        'customers': customers,
    }
    return render(request, 'edit_good.html', context)

@login_required(login_url='login')
def goods_list(request):
    goods = Goods.objects.filter(user=request.user).order_by('-date_added')  # Filter goods by the logged-in user
    return render(request, 'goods_list.html', {'goods': goods})


def search_goods(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Goods.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            user=request.user  # Filter results by the logged-in user
        )

    return render(request, 'search_output.html', {
        'results': results,
        'query': query,
    })


def delete_good(request, pk):
    good = get_object_or_404(Goods, pk=pk, user=request.user)  # Ensure the good belongs to the user
    good.delete()
    return redirect('goods_list')


def category_list(request):
    # Check if the request method is POST to create a new category
    if request.method == 'POST':
        name = request.POST.get('category-name')
        if name:
            # Create a new category associated with the current user
            Category.objects.create(name=name, user=request.user)
            return redirect('category_list')  # Redirect to the category list after creation

    # Fetch only categories that belong to the currently logged-in user
    categories = Category.objects.filter(user=request.user)
    
    # Render the template with the filtered categories
    return render(request, 'category_list.html', {'categories': categories})



@login_required(login_url='login')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)  # Category is not user-specific
    if request.method == 'POST':
        name = request.POST.get('category-name')
        if name:
            category.name = name
            category.save()
            return redirect('category_list')  # change to your category list URL name
    return render(request, 'edit_category.html', {'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')

from django.contrib import messages
@login_required(login_url='login')
def barcode_scanner(request):
    # Filter categories and customers by the logged-in user
    categories = Category.objects.filter(user=request.user)  # Only categories belonging to the logged-in user
    customers = Customer.objects.filter(user=request.user)  # Only customers belonging to the logged-in user

    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        customer_id = request.POST.get('customer')

        # Validation
        if not barcode or not name or not quantity or not price or not description or not category_id or not customer_id:
            messages.error(request, "All fields must be filled out.")
            return redirect('barcode_scanner')

        try:
            # Ensure the category and customer belong to the logged-in user
            category = Category.objects.get(id=category_id, user=request.user)  
            customer = Customer.objects.get(id=customer_id, user=request.user)  
        except Category.DoesNotExist or Customer.DoesNotExist:
            messages.error(request, "Invalid category or customer selection.")
            return redirect('barcode_scanner')

        try:
            # Save the product
            product = Goods.objects.create(
                barcode=barcode,
                name=name,
                quantity=int(quantity),
                price=float(price),
                description=description,
                category=category,
                customer=customer,
                user=request.user  # Associate the product with the logged-in user
            )
            messages.success(request, "Product added successfully!")
            return redirect('dashboard')
        except ValueError:
            messages.error(request, "Invalid quantity or price entered.")
            return redirect('barcode_scanner')

    return render(request, 'barcode_scanner.html', {'categories': categories, 'customers': customers})



def barcode_retrieve(request):
    product = None
    barcode = None  # Initialize barcode variable

    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        print(f"Received barcode: {barcode}")  # Debugging print statement

        if barcode:
            try:
                product = Goods.objects.get(barcode=barcode, user=request.user)  # Ensure the product belongs to the user
            except Goods.DoesNotExist:
                product = None
                messages.error(request, "Product not found.")

    return render(request, 'barcode_retrieve.html', {'product': product, 'barcode': barcode})
