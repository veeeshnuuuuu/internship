from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Transaction

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['email'].label = "Email Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['phone'].label = "Phone Number"

        self.fields['username'].help_text = None
        self.fields['email'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'description']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'category': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': '0.01', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].label = "Transaction Type"
        self.fields['category'].label = "Category"
        self.fields['amount'].label = "Amount (₹)"
        self.fields['description'].label = "Description"