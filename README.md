- Nama: **Muhammad Abyasa Pratama**
- NPM: **2306207663**
- Kelas: **F**
 
[Tautan menuju Aplikasi](http://muhammad-abyasa-netbuy.pbp.cs.ui.ac.id/)

1. Pada dasarnya, JavaScript berfungsi dalam membuat suatu aplikasi web menjadi lebih interaktif dan dinamis. Penggunaan JavaScript dalam suatu aplikasi web di antaranya dalam melakukan proses validasi form, memodifikasi struktur/tampilan HTML dan CSS dalam page secara dinamis, menjalankan _event handling_ berdasarkan aktivitas user dalam web, serta melakukan pengiriman data secara asinkronus menggunakan AJAX.

2. Fungsi `await()` berguna untuk menghentikan eksekusi suatu kode/fungsi hingga proses pengambilan data yang dilakukan fungsi `fetch()` selesai dijalankan. Tanpa penggunaan fungsi `await()`, suatu fungsi yang melakukan pengaksesan terhadap data akan tetap berjalan meskipun data yang dibutuhkan belum selesai diambil oleh fungsi `fetch()`. Hal ini kemudian dapat menyebabkan berbagai permasalahan/_error_ ketika fungsi tersebut melakukan proses pengaksesan data yang belum tersedia.

3. Penggunaan _decorator_ `csrf_exempt` bertujuan untuk melewati pengecekan `csrf_token` pada suatu _request_. Dengan menggunakan `csrf_exempt` pada _view_, Django tidak akan melakukan proses validasi `csrf_token` pada POST _request_ yang dikirim oleh AJAX. Hal ini penting karena secara _default_, POST _request_ yang dikirim oleh AJAX tidak memuat `csrf_token`.

4. Pembersihan data di _backend_ merupakan suatu hal yang penting karena pembersihan pada _frontend_ (seperti penggunaan DOMpurify yang melakukan pembersihan pada sisi HTML) tidak bisa menjamin bahwa data baru tersebut  aman untuk disimpan dalam _database_. Pembersihan data di _backend_ juga berguna untuk mem-_filter_ data-data yang dikirim selain melalui metode konvensional (input _user_ pada _page_), misalnya melalui API eksternal yang keamanannya belum tentu terjamin.

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
            htmlString += `
            <div class="relative break-inside-avoid">
                <div class="relative top-5 bg-white shadow-[0_1px_15px_rgba(0,0,0,0.4)] hover:shadow-[0_1px_20px_rgba(0,0,0,0.5)] rounded-xl mb-6 break-inside-avoid flex flex-col transform transition-transform duration-300">
                    <div class="bg-orange-500 text-white p-4 py-3 rounded-xl">
                        <h3 class="font-bold text-xl">${item.fields.name}</h3>
                    </div>
                    <div class="p-4">
                        <p class="font-semibold text-base mb-1">Description</p>
                        <p class="text-gray-700 text-base mb-2">
                            <span class="pb-1">${item.fields.description}</span>
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
Kemudian, buatlah _modal form_ dengan Tailwind pada `main.html` seperti pada kode berikut:
```
<div id="crudModal" tabindex="-1" aria-hidden="true" class="hidden fixed inset-0 z-50 w-full flex items-center justify-center bg-gray-800 bg-opacity-50 overflow-x-hidden overflow-y-auto transition-opacity duration-300 ease-out">
    <div id="crudModalContent" class="relative bg-white rounded-lg shadow-lg w-5/6 sm:w-3/4 md:w-1/2 lg:w-1/3 mx-4 sm:mx-0 transform scale-95 opacity-0 transition-transform transition-opacity duration-300 ease-out">
        <!-- Modal header -->
        <div class="flex items-center justify-between p-4 border-b rounded-t">
        <h3 class="text-xl font-semibold text-gray-900">
            Add New Item
        </h3>
        <button type="button" class="text-gray-400 bg-transparent hover:bg-yellow-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" id="closeModalBtn">
            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
            <span class="sr-only">Close modal</span>
        </button>
        </div>
        <!-- Modal body -->
        <div class="px-6 py-4 space-y-6 form-style">
        <form id="shopEntryForm">
            <div class="mb-4">
            <label for="name" class="block text-sm font-medium text-gray-700">Item Name</label>
            <input type="text" id="name" name="name" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-orange-500" placeholder="Item name" required>
            </div>
            <div class="mb-4">
            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
            <textarea id="description" name="description" rows="3" class="mt-1 block w-full h-52 resize-none border border-gray-300 rounded-md p-2 hover:border-orange-500" placeholder="Item Description" required></textarea>
            </div>
            <div class="mb-4">
            <label for="price" class="block text-sm font-medium text-gray-700">Price</label>
            <input type="number" id="price" name="price" min="1000" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-orange-500" required>
            </div>
        </form>
        </div>
        <!-- Modal footer -->
        <div class="flex flex-col space-y-2 md:flex-row md:space-y-0 md:space-x-2 p-6 border-t border-gray-200 rounded-b justify-evenly">
        <button type="button" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-5 rounded-full" id="cancelButton">Cancel</button>
        <button type="submit" id="submitShopEntry" form="shopEntryForm" class="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-2 px-5 rounded-full">Save</button>
        </div>
    </div>
</div>
```
Agar _modal form_ tersebut bisa berfungsi, tambahkan fungsi-fungsi berikut pada _block script_:
```
const modal = document.getElementById('crudModal');
const modalContent = document.getElementById('crudModalContent');

function showModal() {
    const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');

    modal.classList.remove('hidden'); 
    setTimeout(() => {
    modalContent.classList.remove('opacity-0', 'scale-95');
    modalContent.classList.add('opacity-100', 'scale-100');
    }, 50); 
}

function hideModal() {
const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');

    modalContent.classList.remove('opacity-100', 'scale-100');
    modalContent.classList.add('opacity-0', 'scale-95');

    setTimeout(() => {
    modal.classList.add('hidden');
    }, 150); 
}

document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalBtn").addEventListener("click", hideModal);
```
Kemudian, tambahkan juga button untuk membuka _modal form_ seperti berikut:
```
<button data-modal-target="crudModal" data-modal-toggle="crudModal" class="border-2 border-yellow-900 text-yellow-900 font-bold hover:bg-yellow-900 hover:border-yellow-900 hover:text-yellow-100 hover:shadow-md py-2 px-4 rounded-full transition duration-300 ease-in-out transform" onclick="showModal();">
    Add New Item by AJAX
</button>
```
Sementara itu, sembunyikan tombol _Add New Item_ yang sebelumnya dengan menambahkan properti `hidden` dalam _tag_ tombol tersebut. Agar form yang baru dibuat bisa digunakan untuk menambah data baru menggunakan AJAX, buatlah fungsi `addShopEntry` pada _block script_ beserta dengan _event listener_ untuk menjalankan fungsi tersebut:
```
  function addShopEntry() {
    fetch("{% url 'main:create_shop_entry_ajax' %}", {
    method: "POST",
    body: new FormData(document.querySelector('#shopEntryForm')),
    })
    .then(response => refreshShopEntries())

    document.getElementById("shopEntryForm").reset(); 
    document.querySelector("[data-modal-toggle='crudModal']").click();

    return false;
  }

  document.getElementById("shopEntryForm").addEventListener("submit", (e) => {
    e.preventDefault();
    addShopEntry();
  })
```

### Implementasi Pencegahan _Cross Site Scripting_ (XSS) ###
Bukalah berkas `views.py` dan `forms.py` lalu tambahkan import `strip_tags` dari `django.utils.html`. Kemudian, tambahkan _strip tags_ pada variabel `name` dan `description` pada fungsi `create_shop_entry_ajax` seperti berikut:
```
def create_shop_entry_ajax(request):
    name = strip_tags(request.POST.get("name"))
    ...
    description = strip_tags(request.POST.get("description"))
    ...
``` 
Lalu, pada berkas `forms.py`, tambahkan dua method seperti berikut pada class `ShopEntryForm`:
```
def clean_name(self):
    name = self.cleaned_data["name"]
    return strip_tags(name)

def clean_description(self):
    description = self.cleaned_data["description"]
    return strip_tags(description)
```

### Implementasi Pembersihan Data dengan DOMPurify ###
Pada berkas `main.html`, tambahkan _script tag_ berikut pada _block meta_:
```
<script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.7/dist/purify.min.js"></script>
```
Kemudian, tambahkan kode berikut dalam fungsi `refreshShopEntries` pada _block script_:
```
async function refreshShopEntries(){
    ...
    if (shopEntries.length === 0) {
        ...
    } else {
        shopEntries.forEach((item) => {
            const name = DOMPurify.sanitize(item.fields.name);
            const description = DOMPurify.sanitize(item.fields.description);
            ...
        });
    }
    ...
}
...
```
Lalu, dalam _htmlString_, ubahlah _template tag_ `item.fields.name` dan `item.fields.description` menjadi `name` dan `description` saja.