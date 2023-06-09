from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Product
from category.models import Category,Sub_Category
from cart.models import Cart, CartItem

from cart.views import _cart_id

# Create your views here.

def home(request):
  featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:5]
  featured_products = Product.objects.all().filter(is_featured=True)[:8]
  off_products = Product.objects.filter(product_offer__gt=0)
  
  context = {
    'featured_categories': featured_categories,
    'featured_products': featured_products,
    'off_products':off_products,
  }
  
  return render(request,'home.html')

def shop(request, category_slug=None, sub_category_slug=None):
  categories_shop= None
  subCategories_shop = None
  products = None
    
  if sub_category_slug != None:
    subCategories_shop = get_object_or_404(Sub_Category, slug=sub_category_slug)
    products = Product.objects.all().filter(sub_category=subCategories_shop, is_available=True)
    product_count = products.count()
    
  elif category_slug != None:
    categories_shop = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.all().filter(category=categories_shop, is_available=True)
    product_count = products.count()
        
  else:
    categories_shop = Category.objects.all()
    subCategories_shop = Sub_Category.objects.all()
    products = Product.objects.all().filter(is_available=True).order_by('product_name')
    product_count = products.count()
  
  sort_by = request.GET.get('sort_by')
  if sort_by == 'price':
        products = products.order_by('price')
  elif sort_by == 'name':
      products = products.order_by('product_name')
    
  if request.method == 'POST':
    min = request.POST['minamount']
    max = request.POST['maxamount']
    min_price = min.split('₹')[1]
    max_price = max.split('₹')[1]
    products = Product.objects.all().filter(Q(price__gte=min_price),Q(price__lte=max_price),is_available=True).order_by('price')
    product_count = products.count()
    
  
  paginator = Paginator(products, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  
    
  context = {
    'categories_shop':categories_shop,
    'subCategories_shop':subCategories_shop,
    'products':page_obj,
    'product_count':product_count
  }
  return render(request,'shop/shop.html',context)


def product_details(request, category_slug, sub_category_slug, product_slug):
    categories = Category.objects.all()
    
    try:
      product = Product.objects.get(category__slug=category_slug, sub_category__slug=sub_category_slug, slug=product_slug)
      in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()    
      related_products = Product.objects.filter(sub_category__slug=sub_category_slug)[:4]
    except Exception as e:
      raise e

    context = {
      'categories':categories,
      'product':product,
      "related_products":related_products,
      "in_cart":in_cart,
    }
    return render(request, 'shop/product_detail.html', context)

def price_change(request):
  var_value = request.GET['var_value']
  pro_id = request.GET['pid']
  product = Product.objects.get(id=pro_id)
  price = product.offer_price()
  x = var_value.split()
  var_value = int(x[0])
  pro_price = price * var_value
  return JsonResponse(
          {'success': True,
           'pro_price':pro_price,
           },
          safe=False
        )
  
def search(request):
  if request.method == 'GET':
    keyword = request.GET['keyword']
    if keyword:
      products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
      product_count = products.count()
      
  paginator = Paginator(products, 9)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
      
  context = {
    'products':page_obj,
    'product_count':product_count,
  }
  return render(request, 'shop/shop.html', context)
  
def contact(request):
  return render(request, 'contact.html')

def sub_category(request):
  cat_id = request.GET['category_id']
  sub_categories = Sub_Category.objects.filter(category=cat_id).values()
  
  return JsonResponse(
          {'success': True,
           'sub_categories':list(sub_categories),
           },
          safe=False
        )