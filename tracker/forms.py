# tracker/forms.py
from django import forms
from .models import Expense
from django.contrib.auth.forms import AuthenticationForm # Para sa built-in na Login Form

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# NEW: Custom LoginForm para sa styling
class LoginForm(AuthenticationForm):
    # Overwrite ang default field widgets para magdagdag ng custom classes
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username', 
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        })
    )