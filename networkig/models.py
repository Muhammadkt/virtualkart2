from django.db import models
from accounts.models import Account
#from orders.models import Address

# Create your models here.
#class Network(models.Model):
 # image = models.ImageField(upload_to='photos/products', blank=True)
 # user_name = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
#  date_of_birth=models.DateField(auto_now_add=True)
#  email = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
#  phone_number = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
#  address_line1 = models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  address_line2 = models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  country = models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  state =models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  district =models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  city =models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  pincode =models.ForeignKey(Address,on_delete=models.CASCADE, null=True)
#  text=models.TextField(max_length=5000, blank=True)
  #def full_name(self):
        # return f"{self.user_name}"