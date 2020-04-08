from django.forms import modelform_factory
from django.shortcuts import render
from .forms import ProductForm, RequestForm
from .models import Product, Request
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def sign_up(request):

    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()

    else:
        signup_form = UserCreationForm()

    return render(request, 'synergy/login.html', {'signup_form': signup_form})


def submit_product(request):

    product_form = modelform_factory(Product, form=ProductForm)

    if request.method == 'POST':
        my_form = product_form(request.POST)

        if my_form.is_valid():
            my_form.save()

    else:
        my_form = product_form()

    return render(request, 'synergy/productform.html', {'my_form': my_form})


def submit_request(request):

    request_form = modelform_factory(Request, form=RequestForm)

    if request.method == 'POST':
        this_form = request_form(request.POST)

        if this_form.is_valid():
            this_form.save()

    else:
        this_form = request_form()

    return render(request, 'synergy/requestform.html', {'this_form': this_form})
