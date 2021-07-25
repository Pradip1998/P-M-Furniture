from django.forms import ModelForm
from furnitureshop.models import Order,Customer,Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class CheckOutForm(ModelForm):
    class Meta:
        model=Order
        fields=["order_by","shipping_address","email","mobile"]
class CreateUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())
    email=forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model=Customer
        fields=['username','email','password1','password2','full_name','address']
    def clean_username(self):
        uname=self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Already Existed User")
        return uname
class Customerloginform(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())












