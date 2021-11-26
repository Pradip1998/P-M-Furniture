from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name="furnitureshop"
urlpatterns = [
    path('', views.index,name='index'),
    path('search',views.SearchView.as_view(),name='search'),
    path('about', views.about,name='about'),
    path('contact', views.contact,name='contact'),
    path('furniture', views.fruniture,name='furniture'),
    path('head', views.head,name='head'),
    path('test', views.test, name='test'),
    path('single/<int:id>', views.single, name='single'),
    path('add-to-cart-<int:pro_id>', views.AddToCartView.as_view(),name='addtocart'),
    path('mycart', views.MyCartView.as_view(),name='mycart'),
    path('manage-cart/<int:cp_id>', views.ManageCart.as_view(),name='managecart'),
    path('emptycart', views.EmptycartView.as_view(),name='emptycart'),
    path('checkout', views.CheckOutView.as_view(),name='checkout'),
    path('register', views.CustomerRegister.as_view(),name='register'),
    path('logout', views.CustomerLogout.as_view(),name='logout'),
    path('login', views.CustomerLogin.as_view(),name='login'),
    path('profile', views.CustomerProfile.as_view(),name='profile'),
    path('reset_password',
         auth_views.PasswordResetView.as_view(template_name="PasswordReset.html"),
         name='reset_password'),
    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name='password_reset_complete'),













]
