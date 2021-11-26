from django.shortcuts import render,redirect,reverse

from . import form
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View,TemplateView,CreateView,FormView
from django.shortcuts import get_object_or_404
from .form import CheckOutForm,CreateUserForm,Customerloginform,Adminloginform
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib.auth.models import Group











# Create your views here.
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        check = Cart.objects.filter(id=cart_id)
        if len(check)>0:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated :
                cart_obj.customer=request.user
                cart_obj.save()


        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = "search.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        kw=self.request.GET.get("keyword")
        results=Product.objects.filter(title__icontains=kw)
        context['results']=results
        return context

def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email=request.POST['email']
        phone = request.POST['phone']
        message=request.POST['message']
        someth=Message(name=name,email=email,phone=phone,message=message)
        someth.save()
        send_mail(name,
                  'Thankyou for your message',
                  'pradipchapagain123@gmail.com',
                  [email])

    Products = Product.objects.filter(discount=False).order_by('-id')
    paginator = Paginator(Products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    discounted_product=Product.objects.filter(discount=True).order_by('-id')
    trending_product=Product.objects.filter(view_count__gte=30)
    Happycustomers=Happycustomer.objects.all()



    contaxt={
        'count':Products.count,
        'Products':Products,
        'page_obj':page_obj,
        'discounted_product':discounted_product,
        'trending_product':trending_product,
        'Happycustomers':Happycustomers

       

    }


    return render(request, 'index.html',contaxt)

def about(request):

    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        someth = Message(name=name, email=email, phone=phone, message=message)
        someth.save()
        send_mail(name,
                  'Thankyou for your message',
                  'pradipchapagain123@gmail.com',
                  [email])

    return render(request,'contact.html')


def fruniture(request):
    Catagories=Catagory.objects.all().order_by('-id')
    contaxt = {
        'count': Catagories.count(),
        'Catagories': Catagories
    }

    return render(request,'furniture.html',contaxt)

def head(request):
    return render(request,'head.html')
def test(request):
    Products = Product.objects.all()

    return render(request,'test.html',{'Products':Products})

def single(request,id):
    Products = Product.objects.get(id=id)
    Products.view_count +=1
    Products.save()

    return render(request,'details.html',{'Products': Products})

class AddToCartView(EcomMixin,TemplateView):
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        product_id=self.kwargs['pro_id']
        product_obj=Product.objects.get(id=product_id)
        cart_id=self.request.session.get("cart_id")
        check = Cart.objects.filter(id=cart_id)
        if len(check)>0:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartptoduct = this_product_in_cart.last()
                cartptoduct.quantaty += 1
                cartptoduct.subtotal += product_obj.selling_price
                cartptoduct.save()
                cart_obj.total_amout += product_obj.selling_price
                cart_obj.save()
            else:
                cartptoduct = Cartproduct.objects.create(cart=cart_obj, product=product_obj,
                                                         rate=product_obj.selling_price, quantaty=1,
                                                         subtotal=product_obj.selling_price)
                cart_obj.total_amout += product_obj.selling_price
                cart_obj.save()



        else:
            cart_obj = Cart.objects.create()
            self.request.session['cart_id'] = cart_obj.id
            cartptoduct = Cartproduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.selling_price,
                                                     quantaty=1, subtotal=product_obj.selling_price)
            cart_obj.total_amout += product_obj.selling_price
            cart_obj.save()

        return context

class ManageCart(EcomMixin,TemplateView):
    def get(self,request,*args, **kwargs):

        cp_id=self.kwargs["cp_id"]
        action=request.GET.get("action")
        cp_obj = Cartproduct.objects.get(id=cp_id)
        cart = cp_obj.cart

        if action== "inc":
            cp_obj.quantaty +=1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart.total_amout += cp_obj.rate
            cart.save()
        elif action=="dcr" :
            cp_obj.quantaty -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart.total_amout -= cp_obj.rate
            cart.save()
            if cp_obj.quantaty ==0:
                cp_obj.delete()

        elif action == "rmv":
            cart.total_amout -= cp_obj.subtotal
            cart.save()
            cp_obj.delete()
            pass

        else:
            pass

        return redirect( 'furnitureshop:mycart' )

class EmptycartView(EcomMixin,View):
    def get(self, request, *args, **kwargs):
        cart_id=self.request.session.get('cart_id',None)
        Check = Cart.objects.filter(id=cart_id)
        if len(Check)>0:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total_amout=0
            cart.save()
        return redirect( 'furnitureshop:mycart' )
class CheckOutView(EcomMixin,CreateView):
    template_name = "shop.html"
    form_class = CheckOutForm
    success_url = reverse_lazy('furnitureshop:index')
    form = CheckOutForm()
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user)

        else:
            return redirect("login?next=/checkout")
        return super().dispatch(request,*args,**kwargs)


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id")
        Check = Cart.objects.filter(id=cart_id)
        form = CheckOutForm()
        if len(Check)>0:
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = None
            context = {
                'cart': cart,
                'form':form,
            }
        else:
            pass
        return context



    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        Check = Cart.objects.filter(id=cart_id)
        if len(Check)>0:
            if cart_id:
                cart_obj= Cart.objects.get(id=cart_id)
                form.instance.cart=cart_obj
                form.instance.subtotal=cart_obj.total_amout
                form.instance.discount=0
                form.instance.total=cart_obj.total_amout
                form.instance.order_status="Order Received"
                del self.request.session["cart_id"]

            else:
                return redirect('furnitureshop:mycart')


        return super().form_valid(form)





class MyCartView(EcomMixin,TemplateView):
    template_name = 'mycart.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id")
        Check = Cart.objects.filter(id=cart_id)
        if len(Check)>0:
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = None
            context = {
                'cart': cart
            }
        else:
            pass
        return context

class CustomerRegister(EcomMixin,CreateView):
    template_name = "Register.html"
    form_class = CreateUserForm
    success_url = reverse_lazy('furnitureshop:login')

    def form_valid(self, form):
        username=form.cleaned_data.get('username')
        password1=form.cleaned_data.get('password1')
        password2=form.cleaned_data.get('password2')
        email=form.cleaned_data.get('email')
        full_name=form.cleaned_data.get('full_name')
        address = form.cleaned_data.get('address')
        customer=Customer.objects.create_user(username=username,password=password1,email=email,full_name=full_name,address=address)
        customer.save()
        group=Group.objects.get(name='customer')
        customer.groups.add(group)
        messages.success("Account created for:"+username)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogout(View):
    def get(self,request):
        logout(request)
        return redirect("furnitureshop:index")



class CustomerLogin(FormView):
    template_name = "login.html"
    form_class = Customerloginform
    success_url =reverse_lazy('furnitureshop:index')
    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        customer = authenticate(self.request, username=username, password=password)
        if customer is not None :
            login(self.request,customer)
        else:
            return render(self.request,self.template_name,{"form":self.form_class,"Error":"Invalid credentials"})



        return super().form_valid(form)
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url=self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustomerProfile(EcomMixin,TemplateView):
    template_name = "Profile.html"


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        customer = self.request.user

        context['customer'] = customer

        orders=Order.objects.filter(cart__customer=customer)
        context['orders'] = orders
        return context


































    

















