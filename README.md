- Nama: **Muhammad Abyasa Pratama**
- NPM: **2306207663**
- Kelas: **F**
 
[Tautan menuju Aplikasi](http://muhammad-abyasa-netbuy.pbp.cs.ui.ac.id/)

1. Pertama-tama, jika suatu elemen HTML memiliki CSS selector yang dibuat secara inline (didefinisikan secara langsung dalam tag HTML), maka selector tersebut yang menjadi prioritas pertama. Misalkan, jika elemen HTML tersebut diberikan atribut warna pada beberapa selector, maka warna yang didefinisikan dalam selector inline yang akan ditampilkan sebagai warna elemen tersebut. Sementara itu, prioritas kedua setelah inline terdapat dalam selector ID dari elemen tersebut. Selector class kemudian menjadi prioritas ketiga dan selector berbasis jenis elemen tersebut (p, div, dll) menjadi prioritas terakhir jika tidak ada definisi dari ketiga selector sebelumnya.

2. _Responsive design_ merupakan konsep yang penting dalam pengembangan web agar suatu aplikasi memiliki tampilan antarmuka yang dinamis. Dengan implementasi _responsive design_, unsur-unsur yang terdapat dalam suatu page menjadi tersusun dengan rapi menyesuaikan dengan ukuran layar atau _window_ device. Penyusunan page secara dinamis membuat user merasa nyaman dalam menggunakan aplikasi tersebut, terlepas dari ukuran device yang digunakan user tersebut. Sebagian besar aplikasi dan website yang beredar sekarang, seperti YouTube dan Instagram, sudah menerapkan responsive design dalam penempatan layout _page_-nya.

3. Dalam suatu elemen HTML, padding merupakan area yang mengatur jarak antara suatu konten (misalkan teks) dengan border-nya. Sementara itu, border merupakan area yang melingkupi suatu konten dan berperan sebagai pembatas luar dari container elemen tersebut. Sementara itu, margin merupakan area yang mengatur jarak antara elemen tersebut dengan elemen-elemen lainnya dalam berkas HTML.

4. Flexbox digunakan untuk menyusun beberapa elemen dalam satu dimensi saja (baik secara horizontal maupun vertikal), di mana tiap elemen bisa diberikan pengaturan _space_ yang digunakan. Sementara itu, grid digunakan untuk menyusun beberapa elemen dalam ruang dua dimensi menggunakan prinsip pembagian baris dan kolom untuk tiap elemennya. Flexbox lebih baik digunakan untuk elemen yang perlu disusun secara linear seperti _navigation bar_. Sementara itu, grid lebih baik digunakan untuk elemen yang perlu disusun dalam suatu ruang, di mana masing-masing elemen bisa diberikan pembagian _space_ yang bervariasi, contohnya seperti penyusunan teks dan berbagai elemen lainnya dalam suatu _page_.

5. Berikut merupakan step-by-step implementasi Tugas 5:

### Menambahkan Tailwind dan Membuat Fungsi Edit & Delete Entry
Pertama-tama, tambahkan script tailwind dalam berkas `base.html` dengan menambahkan `<script src="https://cdn.tailwindcss.com"></script>` pada bagian _head_ agar _framework_ tailwind bisa digunakan pada _template_. Setelah itu, bukalah berkas `views.py` dan buatlah fungsi `edit_item` yang berfungsi untuk mengubah detail dari suatu entry seperti berikut:
```
def edit_item(request, id):
    item = ShopEntry.objects.get(pk = id)
    form = ShopEntryForm(request.POST or None, instance=item)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_item.html", context)
```
Setelah itu, buatlah berkas `edit_item.html` pada direktori `main/templates` yang berfungsi sebagai template untuk page edit entry. Kemudian, import fungsi yang sudah dibuat pada `views.py` dan tambahkan routing URL terhadap path seperti berikut:
```
path('edit-item/<uuid:id>', edit_item, name='edit_item'),
```
Bukalah pula berkas `main.html` pada `main/templates` dan tambahkan elemen button untuk mengedit entry pada elemen tabel yang menampilkan data tiap entry. Selanjutnya, pada berkas `views.py`, buatlah fungsi `delete_item` yang berfungsi untuk menghapus suatu entry seperti berikut:
```
def delete_item(request, id):
    item = ShopEntry.objects.get(pk = id)
    item.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
```
Kemudian, import-lah fungsi tersebut dalam berkas `views.py` dan tambahkan routing URL seperti berikut:
```
path('delete/<uuid:id>', delete_mood, name='delete_mood'),
```

### Konfigurasi Static Files
Bukalah berkas settings.py dan pada bagian _middleware_, tambahkan WhiteNoise di bawah SecurityMiddleWare:
```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```
Kemudian, aturlah konfigurasi untuk STATIC_URL, STATICFILES_DIRS, dan STATIC_URL seperti berikut:
```
STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static'
    ]
else:
    STATIC_ROOT = BASE_DIR / 'static'
```

### Membuat Styling dengan CSS
Selanjutnya, buatlah direktori `static/css` pada _root directory_ dan buatlah berkas `global.css` pada direktori tersebut. Agar `styling` yang dibuat pada berkas tersebut dapat digunakan dalam semua berkas `template`, tambahkan _link_ pada bagian _head_ berkas `base.html` seperti berikut:
```
<link rel="stylesheet" href="{% static 'css/global.css' %}"/>
```
Selanjutnya, buatlah berkas `navbar.html` pada subdirektori templates pada root directory. Buatlah suatu _navigation bar_ dengan bantuan penggunaan _container_ `<div>` dan FlexBox untuk mengatur _layout_ tiap elemen (_title_, keterangan nama akun, dan _button logout_) secara horizontal (atau vertikal untuk versi _mobile_). Setelah _navbar_ dibuat, tambahkan _template tag_ `{% include 'navbar.html' %}` dalam berkas `main.html`, `edit_item.html`, dan `create_shop_entry.html`.

Kemudian, buatlah berkas `card_info.html` dan `card_item.html` pada subdirektori `main/templates`. Di sini, card_info.html merupakan digunakan sebagai _template card_ yang menampilkan informasi berupa nama akun _user_. Sementara itu, card_item.html digunakan sebagai _template card_ yang menampilkan instansi dari tiap entry yang sudah dibuat. _Card_ ini menampilkan seluruh informasi mengenai data entry (nama, deskripsi, dan harga) serta memiliki dua _button_, masing-masing untuk meng-_edit_ entry dan menghapus entry.

Selanjutnya, buatlah subdirektori `static/images` dan tambahkan berkas gambar `empty.png` dalam subdirektori tersebut. Setelah itu, tambahkan elemen CSS pada berkas `main.html` untuk menambahkan _styling_ pada _page_ utama. Tambahkan pula _card_ yang menampilkan nama akun _user_ pada bagian atas _page_ dengan _template tag_ `{% include "card_info.html" with value=name %}`. Tampilkan pula tiap entry yang sudah dibuat menggunakan _item card_ yang sudah dibuat pada berkas `card_item.html` seperti berikut:
```
{% if not shop_entries %}
<div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
    <img src="{% static 'image/empty.png' %}" alt="Empty" class="w-32 h-32 mb-4"/>
    <p class="text-center text-gray-600 mt-4">No items added yet.</p>
</div>
{% else %}
<div class="columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6 w-full">
    {% for item in shop_entries %}
        {% include 'card_item.html' with item=item %}
    {% endfor %}
</div>
{% endif %}
```
Dapat dilihat bahwa jika belum ada entry yang dibuat, gambar `empty.png` akan ditampilkan pada _page_ beserta dengan keterangan. Setelah _page_ utama selesai dikustomisasi, tambahkan pula elemen CSS pada berkas `login.html` dan `register.html` untuk menambahkan styling pada _page_ _login_ dan _register_.