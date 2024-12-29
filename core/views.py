from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404

#imoort out models
from userauths.models import User
from .models import Product, Category
from cart.models import CartOrder, CartOrderItems, Address

# Landing Page View
class LandingPageView(View):
    def get(self, request):
        return render(request, 'core/landing.html')

# Index View to Display Products
def index(request):
    products = Product.objects.all().order_by("-id")  # Fetch all products and disply them based on the latest product added to the database.
    featured_products = Product.objects.filter(product_status='published', featured=True).order_by("-id")

    context = {
        'products': products, # All products
        'featured_products': featured_products  # Featured products
    }

    return render(request, 'core/index.html', context)

# Index View to Display Products by category
def products_by_category(request, category_name):
    category = get_object_or_404(Category, title=category_name)
    products = Product.objects.filter(category=category)

    context = {
        'products': products, # All products in the category
        'category': category
    }
    return render(request, 'core/products_category.html', context)


def product_list_view(request):
    products = Product.objects.all()
    context = {
        'products': products, # All products
    }

    return render(request, 'core/product-list.html', context)



def category_list_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories, # All Categories
    }

    return render(request, 'core/category-list.html', context)


def view_orders(request):
    user = User.objects.get(id=request.user.id)
    total_price = -1
    total_qty = -1
    customer_orders = []
    for ord in CartOrder.objects.filter(user=user):
        items = []
        subtotal = 0
        address = Address.objects.get(order=ord)
        for item in CartOrderItems.objects.filter(order=ord):
            items.append(item)
            print(item.total_price)
            subtotal = subtotal + float(item.total_price)
        customer_orders.append((ord,address,items))
        total_qty = len(items)
        subtotal
        taxes = round(subtotal * 0.0825, 2)
        total_price = round(subtotal + taxes, 2)
    
    return render(request, 'core/orders.html', {'customer_orders':customer_orders,'total_qty':total_qty, 'total_price':total_price})

def view_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'core/detailed_product.html',{'product':product})
