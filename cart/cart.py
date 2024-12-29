from core.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Check if a session exists
        cart = self.session.get('cart', {})

        # Create a session if not
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        # Make the cart global to the site
        self.cart = cart


    '''
    Method to add an item into the cart
    '''
    def add(self, product, quantity):
        product_id = str(product.id)

        # Check if the product is in the cart
        if product_id in self.cart:
            # Get the old data
            old_qty = int(self.cart[product_id]['qty'])
            old_price = float(self.cart[product_id]['unit_price'])

            # Calculate the new data
            new_qty = old_qty + quantity
            new_price = round(old_price * new_qty, 2)

            # Assign the new data to the cart
            self.cart[product_id]['qty'] = str(new_qty)
            self.cart[product_id]['total_price'] = str(new_price)
        else:
            # Add the new product to the cart
            self.cart[product_id] = {'qty': str(quantity), 'unit_price': str(product.price), 'total_price': str(product.price * quantity)}

        # Mark the session as modified
        self.session.modified = True

    '''
    Method to calculte the total quantity of items in the cart
    '''
    def get_qty(self):
        qty = 0
        for item in self.cart:
            qty += int(self.cart[item]['qty'])
        return qty

    '''
    Method to calculte the total price of items in the cart
    ''' 
    def get_item_qty(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]['qty']
        return 0

    '''
    Method to update a product in the cart
    '''
    def get_price(self):
        price = 0.00
        for item in self.cart:
            price += float(self.cart[item]['total_price'])
        return price

    def get_items(self):
        item_ids = self.cart.keys()
        items_in_cart = Product.objects.filter(id__in=item_ids)
        return items_in_cart

    '''
    Method to update a product in the cart
    '''
    def update(self, product, quantity):
        product_id = str(product.id)

        # If the product is in the cart, update the quantity
        if product_id in self.cart:
            # Get old data
            old_qty = int(self.cart[product_id]['qty'])
            old_price = float(self.cart[product_id]['unit_price'])

            # Update the quantity
            new_qty = quantity
            new_price = round(old_price * new_qty, 2)

            # Update the cart data
            self.cart[product_id]['qty'] = str(new_qty)
            self.cart[product_id]['total_price'] = str(new_price)

        # Mark the session as modified
        self.session.modified = True


    '''
    Method to remove an item from the cart
    '''
    def remove(self, product):
        product_id = str(product.id)

        # Remove the product from the cart
        removed_item = self.cart.pop(product_id, None)
        
        # Mark the session as modified
        self.session.modified = True
        return removed_item
    
    '''
    Method to empty cart
    '''
    def empty(self):
        self.cart.clear()
        self.session.modified = True
        print("Cart emptied")
