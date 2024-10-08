- Nama: **Muhammad Abyasa Pratama**
- NPM: **2306207663**
- Kelas: **F**
 
[Tautan menuju Aplikasi](http://muhammad-abyasa-netbuy.pbp.cs.ui.ac.id/)

1. 

2. 

3. 

4. 

5. Berikut merupakan step-by-step implementasi Tugas 6:

Pertama-tama, masuklah ke berkas `views.py` dan tambahkan method untuk menampilkan pesan error pada fungsi `login_user` seperti di bawah ini:
```
if form.is_valid():
    ...
else:
    messages.error(request, "Invalid username or password. Please try again.")
```

### Implementasi AJAX pada Form Entry ###
Pada berkas views.py, tambahkan _import_ `csrf_exempt` dari `django.views.decorators.csrf` dan `require_POST` dari `django.views.decorators.http`. Lalu, buatlah fungsi `create_shop_entry_ajax` untuk membuat entry baru berdasarkan _request_ POST seperti berikut:
```
@csrf_exempt
@require_POST
def create_shop_entry_ajax(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    user = request.user

    new_shop_entry = ShopEntry(
        name=name,
        price=price,
        description=description,
        user=user
    )
    new_shop_entry.save()

    return HttpResponse(b"CREATED", status=201)
```
Setelah itu, buatlah routing URL untuk fungsi tersebut dalam berkas views.py dengan meng-_import_ fungsi tersebut dan menambahkan path seperti berikut:
```
path('create-ajax', create_shop_entry_ajax, name='create_shop_entry_ajax'),
```
Selanjutnya, bukalah kembali berkas views.py dan pada fungsi `show_main`, hapuslah baris `shop_entries = ShopEntry.objects.filter(user=request.user)` dan `'shop_entries': shop_entries,`. Kemudian, pada fungsi show_xml dan show_json, modifikasi baris `data = ShopEntry.objects.all()` menjadi `data = ShopEntry.objects.filter(user=request.user)`. Setelah itu, bukalah berkas `main.html` dan hapuslah _conditional logic_ yang berfungsi untuk menampilkan _item card_ pada halaman utama. Gantilah conditional logic tersebut dengan `div` berikut:
```
<div id="shop_entry_cards"></div>
```
Lalu, pada bagian bawah _endblock content_, tambahkan _block script_ `<script> </script>` untuk menambahkan fungsi-fungsi AJAX. Dalam _block script_ tersebut, tambahkan fungsi `getShopEntries` seperti berikut:
```
async function getShopEntries(){
    return fetch("{% url 'main:show_json' %}").then((res) => res.json())
}
```
Lalu, buatlah fungsi bernama `refreshShopEntries` dalam _block script_ seperti berikut:
```
  async function refreshShopEntries() {
    document.getElementById("shop_entry_cards").innerHTML = "";
    document.getElementById("shop_entry_cards").className = "";
    const shopEntries = await getShopEntries();
    let htmlString = "";
    let classNameString = "";

    if (shopEntries.length === 0) {
        classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
        htmlString = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <img src="{% static 'image/empty.png' %}" alt="Empty" class="w-32 h-32 mb-4"/>
                <p class="text-center text-gray-600 mt-4">No items added yet.</p>
            </div>
        `;
    }
    else {
        classNameString = "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full"
        shopEntries.forEach((item) => {
            const name = DOMPurify.sanitize(item.fields.name);
            const description = DOMPurify.sanitize(item.fields.description);
            htmlString += `
            <div class="relative break-inside-avoid">
                <div class="relative top-5 bg-white shadow-[0_1px_15px_rgba(0,0,0,0.4)] hover:shadow-[0_1px_20px_rgba(0,0,0,0.5)] rounded-xl mb-6 break-inside-avoid flex flex-col transform transition-transform duration-300">
                    <div class="bg-orange-500 text-white p-4 py-3 rounded-xl">
                        <h3 class="font-bold text-xl">${name}</h3>
                    </div>
                    <div class="p-4">
                        <p class="font-semibold text-base mb-1">Description</p>
                        <p class="text-gray-700 text-base mb-2">
                            <span class="pb-1">${description}</span>
                        </p>
                        <div class="mt-6 flex items-center justify-between">
                            <div class="flex">
                              <span class="font-semibold inline-block py-1 px-3 uppercase rounded-full text-orange-600 bg-yellow-200">
                              IDR ${item.fields.price}
                              </span>
                            </div>
                            <div class="flex">
                                <a href="/edit-item/${item.pk}" class="bg-green-400 hover:bg-green-600 text-white rounded-full p-2 transition duration-300 shadow-md mr-2">
                                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                  </svg>
                                </a>
                                <a href="/delete/${item.pk}" class="bg-red-400 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `;
        });
    }
    document.getElementById("shop_entry_cards").className = classNameString;
    document.getElementById("shop_entry_cards").innerHTML = htmlString;
}
refreshShopEntries();
```
