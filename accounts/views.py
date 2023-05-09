from django.shortcuts import render,redirect
from .form import RegistrationForm,AddressForm,UserForm
from .models import Account
from django.contrib import messages, auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from orders.models import Address,Order,OrderProduct
from django.core.paginator import Paginator
from django.http import HttpResponse
#verification email
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



# Create your views here.
def register(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      
      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
      user.save()
      #user activation

      # Generate OTP
      otp = get_random_string(length=4, allowed_chars='1234567890')
        
        # Save user details to database
        # Send OTP to user email
      print(otp)
      subject = 'OTP for account verification'
      message = f'Your OTP for account verification is {otp}'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [email,]
      send_mail(subject, message, email_from, recipient_list)

      user.otp=otp
      user.save()


      # current_site=get_current_site(request)
      # mail_subject='please activate your mail'
      # message=render_to_string('accounts/account_verification_email.html',{'user':user,
      #     'domain':current_site,
      #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
      #     'token':default_token_generator.make_token(user),}
                              
      # )
         
      # to_email=email
      # send_email=EmailMessage(mail_subject,message,to=[to_email])
      # send_email.send()


      
      
      
      messages.success(request, 'Registration Successful')  # registration without otp
      return redirect ('verify_otp',user.id)
  else:    
    form = RegistrationForm()
  context = {
    'form': form
  }
  
  return render (request, 'accounts/register.html', context)

def verify_otp(request, user_id):
    
    user = Account.objects.get(id=user_id)
    
    if request.method == 'POST':
        otp = request.POST['otp']
        if user.otp == otp:
            
            user.otp = ''
            user.is_active=True
            user.save()
            
            messages.success(request, 'Account has been verified')
            return redirect(userLogin)
        
        else:
            messages.error(request, 'Invalid OTP')
            
            return redirect('verifyotp', user_id)
    return render(request, 'accounts/otpVerification.html', {'user': user})

def activate(request,uidb64,token):
   try:
      uid=urlsafe_base64_decode(uidb64).decode()
      user=Account._default_manager.get(pk-uid)
   except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
      user=None
   if user is not None and default_token_generator.check_token(user,token):
      user.is_active=True
      user.save()
      messages.success(request,'congradulation your account is activated')
      return redirect('login')
   else:
      messages.error(request,'invalid activation link')
      return redirect(register)
   
      
      



def userLogin(request):
       if 'username' in request.session:
        return redirect('home')
       elif request.method == 'POST': 
          username =request.POST['email'] 
          password = request.POST['password'] 
          user = auth.authenticate(username=username, password=password)
          if user is not None: 
               request.session['username'] = username 
               auth.login(request,user)
               return redirect('home')
          else: 
               messages.info(request,'Invalid Username or Password') 
               return redirect('userLogin') 
       else: 
          return render(request, 'accounts/login.html')
    
    



def userLogout(request):
  auth.logout(request)
  messages.success(request, "You are logged out.")
  return redirect('home')

@login_required(login_url='userLogin')
def myOrders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders':page_obj
    }

    return render(request,'user/myOrders.html',context)

@login_required(login_url='userLogin') 
def orderDetails(request,order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
        
    context = {
        'order_details':order_details,
        'order':order,
        'subtotal':subtotal    
    }

    return render(request,'user/orderDetails.html',context)

@login_required(login_url = 'userLogin')
def userDashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id= request.user.id, is_ordered= True)
    orders_count = orders.count()
    context = {
        'orders_count':orders_count,
        'orders':orders

    }
    return render(request, 'user/userDashboard.html', context)



@login_required(login_url='userLogin') 
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  
  context = {
    'address':address,
  }
  return render(request, 'user/myAddress.html', context)

@login_required(login_url='userLogin')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.district =  form.cleaned_data['district']
            detail.country=form.cleaned_data['country']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.pincode =  form.cleaned_data['pincode']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('myAddress')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('myAddress')
    else:
        form = AddressForm()
        context={
            'form':form
        }    
    return render(request,'user/add-address.html',context)

@login_required(login_url='userLogin')
def edit_address(request, id):
  address = Address.objects.get(id=id)
  if request.method == 'POST':
    form = AddressForm(request.POST, instance=address)
    if form.is_valid():
      form.save()
      messages.success(request , 'Address Updated Successfully')
      return redirect('myAddress')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('myAddress')
  else:
      form = AddressForm(instance=address)
      
  context = {
            'form' : form,
        }
  return render(request , 'user/edit-address.html' , context)

@login_required(login_url='userLogin')
def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('myAddress')

@login_required(login_url='userLogin') 
def editProfile(request):
  if request.method =='POST':
    form = UserForm(request.POST,instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request,'Your Profile Updated Successfully ')
      return redirect ('userDashboard')

  else:
      form = UserForm(instance=request.user)

  context = {
        'form':form
    } 

  return render(request,'user/editProfile.html', context)
