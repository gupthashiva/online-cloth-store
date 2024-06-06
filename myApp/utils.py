# utils.py

def add_to_cart(request, product_id, quantity):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart
    print(cart)
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart

def update_cart_quantity(request, product_id, quantity):
    cart = request.session.get('cart', {})
    cart[product_id] = quantity
    request.session['cart'] = cart
