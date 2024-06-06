
from django import template

register = template.Library()
'''
@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    print(product, cart)
    keys = cart.keys()
    for id in keys:
        
        if int(id) == product.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
  keys = cart.keys()
  print(keys)
  for id in keys:
      if int(id) == product.id:
        return cart.get(id)
   
  return 0

'''


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    id = product.id
    id_str = str(id)

    if cart and id_str in cart and cart[id_str] != 'null':
        return True
    else:
        return False



@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    id = product.id  # Get the ID of the product
    id_str = str(id)  # Convert the ID to a string for comparison

    if id_str in cart:
        return cart[id_str]
    else:
        return 0



@register.filter(name='price_total')
def price_total(product  , cart):
    return product.price * cart_quantity(product , cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)

    return sum
    