from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from main.forms import ShopEntryForm
from main.models import ShopEntry

# Create your views here.
def show_main(request):
    shop_entries = ShopEntry.objects.all()

    context = {
        'name': 'Muhammad Abyasa Pratama',
        'class': 'PBP F',
        'shop_entries': shop_entries
    }
    return render(request, "main.html", context)

def create_shop_entry(request):
    form = ShopEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "create_shop_entry.html", context)

def show_xml(request):
    data = ShopEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ShopEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ShopEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ShopEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
