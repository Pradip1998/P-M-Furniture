from django.shortcuts import render,redirect,reverse
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View,TemplateView,CreateView,FormView
from django.shortcuts import get_object_or_404
from furnitureshop.form import CheckOutForm,CreateUserForm,Customerloginform,Adminloginform
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from furnitureshop.decorators import allowed_users
from django.contrib.auth.models import Group



class Adminlogin(FormView):
    template_name = 'Asmin/login.html'
    form_class = Adminloginform
    success_url = reverse_lazy('Admin:admin-home')
    def form_valid(self, form):
        username =form.cleaned_data.get('ausername')
        password =form.cleaned_data.get('apassword')
        user= authenticate(self.request, username=username, password=password)
        if user  is not None and user.is_superuser:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "Error": "Invalid credentials"})


        return super().form_valid(form)




@login_required(login_url="Admin:admin-login")
@allowed_users(allowed_roles=['admin'])
def Adminhome(request):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            pass
        else:
            return redirect('/admin-login')

        return super().dispatch(request, *args, **kwargs)

    return render(request,'Asmin/asminindex.html')
