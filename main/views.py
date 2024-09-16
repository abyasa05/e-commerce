from django.shortcuts import render, redirect
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