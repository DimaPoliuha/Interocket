from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate

from .models import TourCategory, Tour, Cart, Order
from .forms import *


def base_view(request):
    tours_categories = TourCategory.objects.all()
    tours = Tour.objects.filter(available=True)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    context = {
        'tours_categories': tours_categories,
        'tours': tours,
        'cart': cart,
    }
    return render(request, 'base.html', context)


def tour_view(request, tour_slug):
    tour = Tour.objects.get(slug=tour_slug)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    context = {
        'tour': tour,
        'cart': cart,

    }
    return render(request, 'tour.html', context)


def category_view(request, category_slug):
    category = TourCategory.objects.get(slug=category_slug)
    tours_of_category = category.tours.all()
    # or
    # tours_of_category = Tour.objects.filter(category=category)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    context = {
        'category': category,
        'tours': tours_of_category,
        'cart': cart,

    }
    return render(request, 'category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    tour_slug = request.GET.get('tour_slug')
    cart.add_to_cart(tour_slug)
    cart.update_total_price()

    return JsonResponse({'cart_total_count': cart.items.count()})


def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    # dynamic delete from cart
    tour_slug = request.GET.get('tour_slug')
    cart.remove_from_cart(tour_slug)

    # dynamic price in cart
    cart.update_total_price()

    return JsonResponse({
        'cart_total_count': cart.items.count(),
        'cart_total': cart.cart_total
    })


def order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    # create form
    form = OrderForm(request.POST or None)

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'order.html', context)


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        Cart.objects.get(id=cart_id)

    form = OrderForm(request.POST or None)

    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        address = form.cleaned_data['address']
        comment = form.cleaned_data['comment']

        Order.objects.create(
            user=request.user,
            tours=cart,
            total_price=cart.cart_total,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            comment=comment,
        )

        del request.session['cart_id']
        del request.session['total']

        context = {
        }

        return render(request, 'checkout.html', context)


def account_view(request):
    orders = Order.objects.filter(user=request.user).order_by('date')
    context = {
        'orders': orders
    }
    return render(request, 'account.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)




        # form.password = form.cleaned_data['password']
        # form.save()
        # login_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
        return HttpResponseRedirect(reverse('login'))
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))

    context = {
        'form': form
    }
    return render(request, 'login.html', context)
