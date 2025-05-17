from django import forms
from .models import *


  
class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['category', 'name', 'quantity', 'description', 'price', 'customer']  # ✅ Include customer here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['customer'].required = False  # optional if you want


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'phone', 'address']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-black rounded px-3 py-2'
            }),
            'email': forms.EmailInput(attrs={
            'class': 'w-full border border-black rounded px-3 py-2',
            'pattern': '^[a-zA-Z0-9._%+-]+@gmail\\.com$',
            'title': 'Only Gmail addresses allowed (e.g. example@gmail.com)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-black rounded px-3 py-2',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '').slice(0,11);",
                'placeholder': 'e.g. 09XXXXXXXXX',
                'maxlength': '11',
                'pattern': '^09\\d{9}$',
                'title': 'Enter a valid Philippine number starting with 09 and 11 digits total'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full border border-black rounded px-3 py-2',
                'rows': 2
            }),
        }

def clean_email(self):
    email = self.cleaned_data['email']
    if not email.endswith('@gmail.com'):
        raise forms.ValidationError("Only Gmail addresses are allowed.")
    return email