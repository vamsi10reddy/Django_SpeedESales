from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from decimal import Decimal
from django.conf import settings
from paypalrestsdk import Payment
from django.urls import reverse
import paypalrestsdk

#import our models
from .cart import Cart
from core.models import Product
from userauths.models import User
from .models import CartOrder, CartOrderItems, Address

# Ensure PayPal SDK is configured
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY
})

# View to display the cart
def view_cart(request):
    cart = Cart(request)

    # Get the items in the cart
    items_in_cart = cart.get_items()
    subtotal = round(cart.get_price(),2)
    taxes = round(subtotal * 0.0825, 2)
    total = round(subtotal + taxes, 2)
    qty = cart.get_qty()

    # Prepare cart data to display
    cart_data = [(product, cart.get_item_qty(product.id)) for product in items_in_cart]

    return render(request, "cart/view_cart.html", {
        "cart_data": cart_data,
        "subtotal": subtotal,
        "taxes": taxes,
        "total": total,
        "qty": qty
    })

# View to add an item to the cart
def add_to_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('id')
        product = Product.objects.get(id=product_id)
        product_qty = int(request.POST.get('qty'))

        # Add product to the cart
        cart.add(product=product, quantity=product_qty)

        # Get updated cart data
        cart_qty = cart.get_qty()
        subtotal = cart.get_price()
        taxes = round(subtotal * 0.0825, 2)
        total = round(subtotal + taxes, 2)

        response = JsonResponse({
            'qty': cart_qty,
            'subtotal': subtotal,
            'taxes': taxes,
            'total': total
        })
        return response

# View to update an item in the cart
def update_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('id'))
        product_qty = int(request.POST.get('qty'))

        # Update the cart with new quantity
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, quantity=product_qty)

        # Get updated cart data
        cart_qty = cart.get_qty()
        subtotal = cart.get_price()
        taxes = round(subtotal * 0.0825, 2)
        total = round(subtotal + taxes, 2)

        # Get item quantity in cart
        item_qty = cart.get_item_qty(product_id)

        response = JsonResponse({
            'item_qty': item_qty,
            'qty': cart_qty,
            'subtotal': subtotal,
            'taxes': taxes,
            'total': total
        })
        return response

# View to remove an item from the cart
def remove_from_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('id'))

        # Remove the product from the cart
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product=product)

        # Get updated cart data
        cart_qty = cart.get_qty()
        subtotal = cart.get_price()
        taxes = round(subtotal * 0.0825, 2)
        total = round(subtotal + taxes, 2)

        response = JsonResponse({
            'qty': cart_qty,
            'subtotal': subtotal,
            'taxes': taxes,
            'total': total
        })
        return response

# View to remove all items from the cart if the user is signed in.
def empty_cart(request):
    if request.method == "POST":
        # Assuming the cart is stored in the session
        request.session['cart'] = {}
        request.session.modified = True
        return JsonResponse({'success': True, 'message': 'Cart emptied successfully'})
    return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)


# Checkout page view
def checkout_page(request):
    cart = Cart(request)
    
    cart_items = []
    # Get cart items and calculate prices
    items_in_cart = cart.get_items()
    for product in items_in_cart:
        product_qty = cart.get_item_qty(product.id)
        total_price = Decimal(product.price) * Decimal(product_qty)
        cart_items.append((product, product_qty, total_price))

    subtotal = sum(item[2] for item in cart_items)
    taxes = round(subtotal * Decimal('0.0825'), 2)  # 8.25% tax
    total_price = round(subtotal + taxes, 2)

    # Check if PayPal is selected
    if request.method == 'POST':
        #get the user's data
        user = User.objects.get(id=request.user.id)

        payment_method = request.POST.get('paymentMethod')
        if payment_method == 'paypal':
            payment = create_paypal_payment(total_price)  # Create PayPal payment
            if payment:
                return redirect(payment.links[1].href)  # Redirect to PayPal
        #if the method is credit card
        elif payment_method == 'credit-card':
            pass
        else:
            #create an order object and save it to the db
            order = CartOrder(user=user, price=total_price)
            order.save()
            #attach the items to the order
            for product,quantity,price in cart_items:
                order_prod = CartOrderItems(order=order,product=product,qty=quantity, unit_price=product.price, total_price=price)
                order_prod.save()
            #save the address for the order
            address = Address(order=order,user=user,send_to=request.POST.get('fullName'),address=request.POST.get('address'),city=request.POST.get('city'),zipCode=request.POST.get('zipCode'))
            address.save()

        #empty the cart and tell the js it was successful
        messages.success(request,("Checkout successful!"))
        cart.empty()
        return JsonResponse({'success': True})

    return render(request, 'cart/checkout.html', {
        'cart_data': cart_items,
        'subtotal': subtotal,
        'taxes': taxes,
        'total': total_price
    })




# Create PayPal payment
def create_paypal_payment(total):
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": f"{total:.2f}",
                "currency": "USD"
            },
            "description": "Online Order"
        }],
        "redirect_urls": {
            "return_url": reverse('cart:payment_success'),
            "cancel_url": reverse('cart:payment_cancel')
        }
    })

    if payment.create():
        return payment
    else:
        # Handle the error, e.g. log the error or return None
        return None

# Payment success handler
def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):  # Confirm the payment
        # Handle successful payment (e.g., update order status, etc.)
        return render(request, 'payment_results.html', {
            'status': 'success',
            'message': 'Payment completed successfully!'
        })
    else:
        # Payment execution failed, log the error
        return render(request, 'payment_results.html', {
            'status': 'failed',
            'message': 'Payment execution failed.'
        })

# Payment cancel handler
def payment_cancel(request):
    # Handle canceled payment (e.g., inform the user)
    return render(request, 'payment_results.html', {
        'status': 'failed',
        'message': 'Payment was canceled.'
    })
