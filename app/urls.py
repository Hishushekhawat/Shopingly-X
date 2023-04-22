from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm , MyPasswordChangeForm ,MyPasswordResetForm , MySetPasswordResetForm
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('showcart/', views.showcart, name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('paymentdone/',views.paymentdone,),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.CustomerProfile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordResetForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/',views.bottomwear,name='bottomwear'),
    path('bottomwear/<slug:data>',views.bottomwear,name='bottomweardata'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),    
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
    path('addproduct/',views.AddProduct.as_view(),name='addproduct'),
    path('allorders/',views.AllOrders,name='allorders'),
    path('orderupdate/<int:pk>',views.OrderUpdate,name='orderupdate'),
    path('removeorder/<int:pk>',views.RemoveOrder,name='removeorder'),
    path('checkout/', views.checkout, name='checkout'),
    path('allproduct/',views.AllProduct,name='allproduct'),
    path('updatedata/<int:pk>',views.UpdateData,name='updatedata'),
    path('delete/<int:pk>',views.Delete,name='delete'),
    path('confirmdelete/<int:pk>/delete',views.ConfirmDelete,name='confirmdelete'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
