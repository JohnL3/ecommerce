from django.shortcuts import render, redirect, reverse

# Create your views here.

def view_cart(request):
    """A view that renders the cart contents page"""
    return render(request, "cart.html")
    
    
def add_to_cart(request, id):
    """Add a quantity of the specified product to the cart"""
    
    if request.POST.get('quantity'):
        quantity=int(request.POST.get('quantity'))
        print('quantity', quantity)
        cart = request.session.get('cart', {})
        cart[id] = cart.get(id, quantity)
        print('cart',cart)
        request.session['cart'] = cart
        return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))
    
    
def adjust_cart(request, id):
    """Adjust the quantity of the specified product to the specified amount"""
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    print('quantity',quantity)
    if quantity > 0:
        cart[id] = quantity
        print('id',id)
        print('cart[id]',cart[id])
        print('cart',cart)
    else:
        cart.pop(id)
        
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
