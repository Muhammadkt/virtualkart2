from django import forms
from .models import Account
from django.contrib import messages
from orders.models import Address



class RegistrationForm(forms.ModelForm):
  
  password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password',
                                                                 }))
  confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                }))
    
  class Meta:
    model = Account
    fields = ['first_name', 'last_name', 'email', 'phone_number',]
    
  def __init__(self, *args, **kwargs):
    super(RegistrationForm,self).__init__(*args, **kwargs)
    self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
    self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
    self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
    self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Mobile Number'
    self.fields['phone_number'].widget.attrs['maxlength'] = 10

    for field  in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
  
  def clean(self):
    cleaned_data = super(RegistrationForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    
    if password != confirm_password:
      raise forms.ValidationError("Password does not match!!")
    
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields  = ['first_name','last_name', 'email', 'phone_number',]

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)  
        for field  in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line1','address_line2','district','country','state','city', 'pincode']
    
    def __init__(self, *args, **kwargs):
      super(AddressForm,self).__init__(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
                          

             
             
