from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from main.forms import ShopEntryForm
from main.models import ShopEntry
import datetime

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    # shop_entries = ShopEntry.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        # 'shop_entries': shop_entries,
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

def create_shop_entry(request):
    form = ShopEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        shop_entry = form.save(commit=False)
        shop_entry.user = request.user
        shop_entry.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "create_shop_entry.html", context)

def show_xml(request):
    data = ShopEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ShopEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ShopEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ShopEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
      else:
        messages.error(request, "Invalid username or password. Please try again.")

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_item(request, id):
    item = ShopEntry.objects.get(pk = id)
    form = ShopEntryForm(request.POST or None, instance=item)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_item.html", context)

def delete_item(request, id):
    item = ShopEntry.objects.get(pk = id)
    item.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def create_shop_entry_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    user = request.user

    new_shop_entry = ShopEntry(
        name=name,
        price=price,
        description=description,
        user=user
    )
    new_shop_entry.save()

    return HttpResponse(b"CREATED", status=201)