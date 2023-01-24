from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phone_objects = Phone.objects.all()

    if request.GET.get('sort') == 'name':
        phone_objects = Phone.objects.all().order_by('name')

    elif request.GET.get('sort') == 'min_price':
        phone_objects = Phone.objects.all().order_by('price')

    elif request.GET.get('sort') == 'max_price':
        phone_objects = Phone.objects.all().order_by('-price')

    context = {'phones': phone_objects}

    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.all().filter(slug=slug)
    context = {'phone': phone[0]}

    return render(request, template, context)
