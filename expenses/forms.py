from django import forms
from django.utils.safestring import mark_safe
from .models import Expenses, Participant, User
from django.forms import modelformset_factory


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ExpenseForm(forms.Form):
    title = forms.CharField(max_length=255)
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    split_method = forms.ChoiceField(choices=[
        ('equal', 'Equal'),
        ('percentage', 'Percentage'),
        ('exact', 'Exact'),
    ])
    description = forms.CharField(max_length=255, required=False)

class ParticipantForm(forms.Form):
    user = forms.CharField(max_length=255)  
    amount_owed = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=False)