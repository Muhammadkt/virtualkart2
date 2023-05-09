from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Wishlist,Product
from accounts.models import Account


@login_required
def wishlist(request):
 wishlist = Wishlist.objects.filter(user=request.user).first()
 products = wishlist.products.all() if wishlist else []
 wishlist_count=products.count()
 context = {'wishlist': wishlist, 'products': products}
 return render(request, 'wishlist/wishlist.html', context)

@login_required
def add_wishlist(request, product_id):
 product = get_object_or_404(Product, pk=product_id)
 wishlist, created = Wishlist.objects.get_or_create(user=request.user)
 wishlist.products.add(product)
 return redirect('wishlist')

@login_required
def remove_wishlist(request, product_id,wishlist_item_id):
 product = get_object_or_404(Product, pk=product_id)
 wishlist = Wishlist.objects.filter(user=request.user).first()
 if wishlist:
  wishlist.products.remove(product)
  return redirect('wishlist')