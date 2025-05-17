
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

from django.contrib import messages



# A simple view function to render the home page
def home(request):
    # Renders and returns the 'home.html' template when a user accesses the home URL
    return render(request, 'home.html')


# Handles user signup
def signup(request):
    # Check if the request method is POST (i.e., form was submitted)
    if request.method == "POST":
        # Get form data from the POST request
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Create a new user using Django's built-in User model and hash the password
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)
        
        # If authentication is successful, log the user in
        if user is not None:
            auth_login(request, user)

        # Redirect the user to the dashboard after successful signup and login
        return redirect("dashboard")

    # If the request is not POST (i.e., GET), render the signup form
    return render(request, 'signup.html')



# Handles user login
def login(request):
    # Check if the form is submitted via POST
    if request.method == "POST":
        # Get the username and password from the submitted form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user using Django's authentication system
        user = authenticate(request, username=username, password=password)

        # If authentication is successful
        if user is not None:
            # Log the user in
            auth_login(request, user)
            # Redirect to dashboard or any other protected page
            return redirect("dashboard")
        else:
            # If credentials are invalid, show login page again with error message
            return render(request, 'login.html', {"error": "Invalid credentials"})

    # If the request is a GET request, just render the login form
    return render(request, 'login.html')



# Restricts access to only logged-in users. If not logged in, redirects to the 'login' page.
@login_required(login_url='login')
def dashboard(request):
    # Get the search query from the GET parameters, or default to an empty string
    query = request.GET.get('q', '')  

    # Initialize variables for editing state
    edit_mode = False
    good_instance = None

    # Get all goods that belong to the currently logged-in user, ordered by newest first
    goods = Goods.objects.filter(user=request.user).order_by('-date_added')  

    # If there's a search query, filter the goods based on name, description, or category name
    if query:
        goods = goods.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # If the URL contains 'edit_good', prepare to edit that specific good
    if 'edit_good' in request.GET:
        edit_mode = True
        good_id = request.GET.get('edit_good')
        # Fetch the good to edit; return 404 if it doesn't exist or doesn't belong to the user
        good_instance = get_object_or_404(Goods, id=good_id, user=request.user)
        # Pre-fill the form with the instance's data
        goods_form = GoodsForm(request.POST or None, instance=good_instance)
    else:
        # Empty form for adding new goods
        goods_form = GoodsForm(request.POST or None)

    # Initialize the category and customer forms
    category_form = CategoryForm(request.POST or None, prefix='category')  # Prefix avoids field name clashes
    customer_form = CustomerForm(request.POST or None)

    # Get categories and customers that belong to the current user
    categories = Category.objects.filter(user=request.user)
    customers = Customer.objects.filter(user=request.user)

    # Handle POST requests (form submissions)
    if request.method == 'POST':
        # If the user submitted the goods form
        if 'submit_good' in request.POST:
            # Use the existing instance if editing
            if good_instance:
                goods_form = GoodsForm(request.POST, instance=good_instance)
            else:
                goods_form = GoodsForm(request.POST)

            if goods_form.is_valid():
                good = goods_form.save(commit=False)
                good.user = request.user  # Associate the good with the current user
                goods_form.save()
                return redirect('dashboard')  # Redirect to clear the form and refresh data

        # If the user submitted the category form
        elif 'submit_category' in request.POST and category_form.is_valid():
            category_form.save()
            return redirect('dashboard')

        # If the user submitted the customer form
        elif 'submit_customer' in request.POST and customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.user = request.user  # Associate the customer with the current user
            customer_form.save()
            return redirect('dashboard')

    # Prepare context data to be sent to the dashboard template
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

    # Render the dashboard with all relevant data
    return render(request, 'dashboard.html', context)



# Restrict access to logged-in users; redirect to 'login' page if not authenticated
@login_required(login_url='login')
def customer_list(request):
    # Get all customers that belong to the current logged-in user, ordered by newest first
    customers = Customer.objects.filter(user=request.user).order_by('-date_added')

    # Initialize the customer form (bind POST data if available)
    form = CustomerForm(request.POST or None)

    # Handle form submission
    if request.method == 'POST':
        # Check if the form is valid
        if form.is_valid():
            # Don't save to the database yet — we need to attach the user first
            customer = form.save(commit=False)
            customer.user = request.user  # Assign the current user to the customer
            form.save()  # Save the customer to the database
            return redirect('customer_list')  # Refresh the page after submission

    # Render the customer list page with the list of customers and the form
    return render(request, 'customer_list.html', {
        'customers': customers,
        'form': form,
    })



# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def edit_customer(request, pk):
    # Get the customer by primary key (pk) and ensure it belongs to the current user
    customer = get_object_or_404(Customer, pk=pk, user=request.user)

    # Initialize the form with POST data (if available) and pre-fill with the existing customer data
    form = CustomerForm(request.POST or None, instance=customer)

    # If the form is submitted
    if request.method == 'POST':
        # Validate and save the changes
        if form.is_valid():
            form.save()
            # Redirect back to the customer list after saving
            return redirect('customer_list')

    # Render the edit form page
    return render(request, 'edit_customer.html', {
        'form': form,
        'customer': customer
    })



# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def delete_customer(request, pk):
    # Retrieve the customer by primary key and ensure it belongs to the current user
    customer = get_object_or_404(Customer, pk=pk, user=request.user)

    # Only allow deletion via POST request to prevent accidental deletes
    if request.method == 'POST':
        customer.delete()  # Delete the customer record
        return redirect('customer_list')  # Redirect to customer list after deletion

    # If not a POST request, redirect to customer list (no deletion happens)
    return redirect('customer_list')




# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def edit_good(request, pk):
    # Retrieve the specific Good object by primary key (pk)
    # and ensure it belongs to the current logged-in user
    good = get_object_or_404(Goods, pk=pk, user=request.user)
    
    # Create the form with POST data if available, and bind it to the existing Good instance
    form = GoodsForm(request.POST or None, instance=good)

    # If the form is submitted and valid, save the updated Good
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')  # Redirect to the dashboard after saving

    # Fetch categories and customers associated with the logged-in user
    categories = Category.objects.filter(user=request.user)
    customers = Customer.objects.filter(user=request.user)

    # Pass the form and related data to the template
    context = {
        'form': form,
        'categories': categories,
        'customers': customers,
    }

    # Render the edit form page
    return render(request, 'edit_good.html', context)


# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def goods_list(request):
    # Retrieve all Goods that belong to the currently logged-in user
    # and order them by the most recently added first
    goods = Goods.objects.filter(user=request.user).order_by('-date_added')

    # Render the goods list template and pass the retrieved goods to the context
    return render(request, 'goods_list.html', {'goods': goods})



# Handles the search functionality for goods
def search_goods(request):
    # Get the search query from the GET request; default to an empty string if not provided
    query = request.GET.get('q', '')
    
    # Initialize an empty list for results
    results = []

    # If a search query is provided, filter the Goods based on the query
    if query:
        results = Goods.objects.filter(
            # Search in the name, description, or category name fields
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            user=request.user  # Ensure the goods belong to the logged-in user
        )

    # Render the search results page and pass the results and query to the template
    return render(request, 'search_output.html', {
        'results': results,
        'query': query,
    })



# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def delete_good(request, pk):
    # Retrieve the specific Good object by primary key (pk)
    # and ensure it belongs to the current logged-in user
    good = get_object_or_404(Goods, pk=pk, user=request.user)

    # Delete the good from the database
    good.delete()

    # Redirect the user to the goods list after deletion
    return redirect('goods_list')


# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def category_list(request):
    # If the request method is POST, handle the creation of a new category
    if request.method == 'POST':
        # Get the category name from the POST data
        name = request.POST.get('category-name')
        
        # If the name is provided, create a new category associated with the logged-in user
        if name:
            Category.objects.create(name=name, user=request.user)
            # Redirect back to the category list after creating the category
            return redirect('category_list')

    # Fetch categories that belong to the logged-in user
    categories = Category.objects.filter(user=request.user)
    
    # Render the template and pass the list of categories to the context
    return render(request, 'category_list.html', {'categories': categories})




# Restrict access to logged-in users; redirect to 'login' if not authenticated
@login_required(login_url='login')
def edit_category(request, pk):
    # Retrieve the category by primary key (pk) — no user filter here as categories are not user-specific
    category = get_object_or_404(Category, pk=pk)

    # If the form is submitted via POST
    if request.method == 'POST':
        # Get the new category name from the POST data
        name = request.POST.get('category-name')
        
        # If a name is provided, update the category
        if name:
            category.name = name  # Update the category's name
            category.save()  # Save the updated category

            # Redirect to the category list after saving the changes
            return redirect('category_list')  # Ensure the URL name corresponds to your category list

    # Render the edit form with the current category data
    return render(request, 'edit_category.html', {'category': category})



def delete_category(request, pk):
    # Retrieve the category by primary key (pk)
    category = get_object_or_404(Category, pk=pk)

    # Delete the selected category
    category.delete()

    # Redirect to the category list page after deletion
    return redirect('category_list')



@login_required(login_url='login')
def barcode_scanner(request):
    # Filter categories and customers to only include those belonging to the logged-in user
    categories = Category.objects.filter(user=request.user)
    customers = Customer.objects.filter(user=request.user)

    if request.method == 'POST':
        # Get the POST data from the form submission
        barcode = request.POST.get('barcode')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        customer_id = request.POST.get('customer')

        # Check if all fields are filled out
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
            # Create a new product and associate it with the logged-in user
            product = Goods.objects.create(
                barcode=barcode,
                name=name,
                quantity=int(quantity),
                price=float(price),
                description=description,
                category=category,
                customer=customer,
                user=request.user
            )
            messages.success(request, "Product added successfully!")
            return redirect('dashboard')
        except ValueError:
            # Handle invalid quantity or price input
            messages.error(request, "Invalid quantity or price entered.")
            return redirect('barcode_scanner')

    # Render the barcode scanner page, passing categories and customers to the template
    return render(request, 'barcode_scanner.html', {'categories': categories, 'customers': customers})



def barcode_retrieve(request):
    product = None  # Initialize the product to None
    barcode = None  # Initialize barcode variable

    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        print(f"Received barcode: {barcode}")  # Debugging print statement

        if barcode:
            try:
                # Retrieve the product by barcode and ensure it belongs to the logged-in user
                product = Goods.objects.get(barcode=barcode, user=request.user)
            except Goods.DoesNotExist:
                # If product is not found, set product to None and show an error message
                product = None
                messages.error(request, "Product not found.")

    # Render the barcode retrieval page, passing the product and barcode to the template
    return render(request, 'barcode_retrieve.html', {'product': product, 'barcode': barcode})
