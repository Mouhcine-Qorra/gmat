from django.forms import ModelForm
from .models import ShippingAdress, Portfolio
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAdress
        fields = ['customer', 'order', 'phone', 'address', 'zipcode', 'state']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'email', 'message']
