
from shop.models import Wishlist

def wish_counter(request) :
  try:
      if 'admin' in request.path:
        return {}
      else:
        try:
          
          if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user).first()
            products = wishlist.products.all() if wishlist else []
            wishlist_count=products.count()
          return dict(wishlist_count=wishlist_count)
        
        except wishlist.DoesNotExist:
          pass
  except:
          pass
     
  return dict(wishlist_count=0)