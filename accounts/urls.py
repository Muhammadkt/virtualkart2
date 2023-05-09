
from django.urls import path
from  .views import *
urlpatterns = [
    path('', userDashboard, name='userDashboard'),
    path('register/', register, name='register'),
    path('login/', userLogin, name='userLogin'),
    path('userLogout/', userLogout, name='userLogouted'),
    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('verify_otp/<int:user_id>', verify_otp, name='verify_otp'),

    path('myOrders/', myOrders, name='myOrders'),
    path('orderDetails/<int:order_id>/', orderDetails, name='orderDetails'),

    path('editProfile/', editProfile, name='editProfile'),
    
    path('myAddress/', myAddress, name='myAddress'),
    path('add_address/', add_address, name='add_address'),
    path('edit_address/<int:id>/', edit_address, name='edit_address'),
    path('delete_address/<int:id>/', delete_address, name='delete_address'),
    
   
] 

