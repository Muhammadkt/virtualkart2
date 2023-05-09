from django.contrib import admin
from .models import *
from .models import Country

# Register your models here.
class OrderProductInline(admin.TabularInline):
  model = OrderProduct
  extra = 0

# class Country(admin.ModelAdmin):
  
#   list_display = ('country_name', 'state', 'district')


class OrderAdmin(admin.ModelAdmin):
  list_display = ['order_number', 'full_name', 'phone', 'email', 'order_total', 'status', 'is_ordered']
  list_per_page =  20
  inlines = [OrderProductInline]

admin.site.register(Payment,)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(UserCoupon)
admin.site.register(Country)







