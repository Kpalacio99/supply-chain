from django import forms
from .models import *

# Form for creating and editing Goods (Products)
class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods  # Use the Goods model
        fields = ['category', 'name', 'quantity', 'description', 'price', 'customer']  # Include category, name, quantity, description, price, and customer fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False  # Make category optional
        self.fields['customer'].required = False  # Make customer optional (can be left blank)


# Form for creating and editing Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category  # Use the Category model
        fields = ['name']  # Only include the 'name' field for the Category form


# Customer form for creating and editing customer details
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer  # Use the Customer model
        fields = ['name', 'email', 'phone', 'address']  # Fields for customer information

        widgets = {
            # Custom widget for 'name' field
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-black rounded px-3 py-2'  # Styling for input
            }),
            # Custom widget for 'email' field with validation for Gmail addresses only
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-black rounded px-3 py-2',  # Styling for input
                'pattern': '^[a-zA-Z0-9._%+-]+@gmail\\.com$',  # Only Gmail pattern
                'title': 'Only Gmail addresses allowed (e.g. example@gmail.com)'  # Tooltip for the user
            }),
            # Custom widget for 'phone' field with a number input restriction
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-black rounded px-3 py-2',  # Styling for input
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '').slice(0,11);",  # Restrict input to digits only
                'placeholder': 'e.g. 09XXXXXXXXX',  # Placeholder for the input field
                'maxlength': '11',  # Max length of 11 digits for Philippine numbers
                'pattern': '^09\\d{9}$',  # Validate phone number format for Philippine numbers
                'title': 'Enter a valid Philippine number starting with 09 and 11 digits total'  # Tooltip for the user
            }),
            # Custom widget for 'address' field with multiline text area
            'address': forms.Textarea(attrs={
                'class': 'w-full border border-black rounded px-3 py-2',  # Styling for input
                'rows': 2  # Set the height of the textarea (2 rows)
            }),
        }

    # Validation for email to ensure it ends with '@gmail.com'
    def clean_email(self):
        email = self.cleaned_data['email']  # Get the email value from the cleaned data
        if not email.endswith('@gmail.com'):  # Check if email does not end with '@gmail.com'
            raise forms.ValidationError("Only Gmail addresses are allowed.")  # Raise validation error
        return email  # Return the email if valid
