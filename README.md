- Nama: **Muhammad Abyasa Pratama**
- NPM: **2306207663**
- Kelas: **F**
 
[Tautan menuju Aplikasi](http://muhammad-abyasa-netbuy.pbp.cs.ui.ac.id/)

1. Pertama-tama, jika suatu elemen HTML memiliki CSS selector yang dibuat secara inline (didefinisikan secara langsung dalam tag HTML), maka selector tersebut yang menjadi prioritas pertama. Misalkan, jika elemen HTML tersebut diberikan atribut warna pada beberapa selector, maka warna yang didefinisikan dalam selector inline yang akan ditampilkan sebagai warna elemen tersebut. Sementara itu, prioritas kedua setelah inline terdapat dalam selector ID dari elemen tersebut. Selector class kemudian menjadi prioritas ketiga dan selector berbasis jenis elemen tersebut (p, div, dll) menjadi prioritas terakhir jika tidak ada definisi dari ketiga selector sebelumnya.

2. Responsive design merupakan konsep yang penting dalam pengembangan web agar suatu aplikasi memiliki tampilan antarmuka yang dinamis. Dengan implementasi responsive design, unsur-unsur yang terdapat dalam suatu page menjadi tersusun dengan rapi menyesuaikan dengan ukuran layar device. Penyusunan page secara dinamis membuat user merasa nyaman dalam menggunakan aplikasi tersebut, terlepas dari ukuran device yang digunakan user tersebut.

3. Dalam suatu elemen HTML, padding merupakan area yang mengatur jarak antara suatu konten (misalkan teks) dengan border-nya. Sementara itu, border merupakan area yang melingkupi suatu konten dan berperan sebagai pembatas luar dari container elemen tersebut. Sementara itu, margin merupakan area yang mengatur jarak antara elemen tersebut dengan elemen-elemen lainnya dalam berkas HTML.

4. Flexbox digunakan untuk menyusun beberapa elemen dalam satu dimensi saja (baik secara horizontal maupun vertikal), di mana tiap elemen bisa diberikan pengaturan _space_ yang digunakan. Sementara itu, grid digunakan untuk menyusun beberapa elemen dalam ruang dua dimensi menggunakan prinsip pembagian baris dan kolom untuk tiap elemennya.

5. Berikut merupakan step-by-step implementasi Tugas 5:

Pertama-tama, tambahkan script tailwind dalam berkas base.html dengan menambahkan `<script src="https://cdn.tailwindcss.com"></script>` pada bagian _head_. Setelah itu, bukalah berkas views.py dan buatlah fungsi edit_item yang berfungsi untuk mengubah detail dari suatu entry seperti berikut:
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
Setelah itu, buatlah berkas edit_item.html pada direktori main/templates yang berfungsi sebagai template untuk page edit entry. Kemudian, import fungsi yang sudah dibuat pada views.py dan tambahkan routing URL terhadap path seperti berikut:
```
path('edit-item/<uuid:id>', edit_item, name='edit_item'),
```
Bukalah pula berkas main.html pada main/templates dan tambahkan elemen button untuk mengedit entry pada elemen tabel yang menampilkan data tiap entry. Selanjutnya, pada berkas views.py, buatlah fungsi delete_item yang berfungsi untuk menghapus entry yang sudah dibuat seperti berikut:
```
def delete_item(request, id):
    item = ShopEntry.objects.get(pk = id)
    item.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
```
Kemudian, import-lah fungsi tersebut dalam berkas views.py dan tambahkan routing URL seperti berikut:
```
path('delete/<uuid:id>', delete_mood, name='delete_mood'),
```