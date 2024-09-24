- Nama: **Muhammad Abyasa Pratama**
- NPM: **2306207663**
- Kelas: **F**
 
[Tautan menuju Aplikasi](http://muhammad-abyasa-netbuy.pbp.cs.ui.ac.id/)

1. `HttpResponseRedirect()` dan `redirect()` sama-sama merupakan fungsi yang digunakan untuk melakukan _redirect_ atau pengalihan user ke _page_ lain, berkaitan dengan suatu aksi yang dilakukan dalam aplikasi. Perbedaan utama antara keduanya adalah bahwa `HttpResponseRedirect()` hanya mampu melakukan _redirect_ menggunakan argumen berupa _string_ URL. Sementara itu, `redirect()` cenderung bersifat lebih fleksibel karena bisa menerima argumen _path_ selain dalam format _string_ URL, termasuk dalam melakukan _URL reversing_ secara otomatis.

2. Penghubungan suatu model objek dengan user bisa dilakukan dengan menambahkan atribut User (yang harus di-_import_ terlebih dahulu) ke dalam class model. Dengan ini, tiap objek model yang tersimpan dalam _database_ akan terasosiasi dengan suatu User. Hal ini bisa dinyatakan sebagai relasi _many-to-one_, di mana suatu user bisa diasosiasikan dengan beberapa objek, sementara tiap objek hanya terasosiasi dengan satu user. Penghubungan antara objek model dengan user bisa dilakukan pada saat pembuatan objek/produk baru (seperti melalui entry form), di mana atribut User dari objek baru tersebut akan diisi dengan user yang menginisiasi pembuatan objek baru itu sendiri (user yang berada pada _session_ tersebut).

3. _Authentication_ merupakan proses untuk memverifikasi apakah suatu _user_ sudah terdaftar dalam sistem aplikasi. Sementara itu, _authorization_ merupakan proses untuk memverifikasi fitur/aksi yang bisa diakses dan digunakan oleh suatu _user_ dalam sistem. Dalam konteks login ke dalam suatu aplikasi, kedua proses ini dijalankan untuk memverifikasi suatu user, pertama untuk memastikan bahwa _user_ menggunakan akun yang sudah terdaftar dalam _database_ aplikasi, dan kedua untuk memastikan jenis akun yang digunakan oleh user (yang kemudian menentukan otoritas user dalam sistem aplikasi). Dalam Django, mekanisme pembuatan akun dilakukan dengan instansiasi objek `User` (di-_import_ dari `django.contrib.auth.models`) yang dilengkapi dengan serangkaian atribut seperti _username_, _email_, _password_, dan lain sebagainya. Sementara itu, proses autentikasi user dibantu dengan penggunaan method `authenticate` dan `login` (di-_import_ dari `django.contrib.auth`), di mana method `authenticate` berfungsi untuk memverifikasi kredensial yang diinput oleh user sementara method `login` akan membuat _session_ baru untuk _user_ yang berhasil melewati proses autentikasi.

4. Jika suatu user melakukan login ke dalam aplikasi, server Django akan membuat suatu _session_ untuk user tersebut. Django juga akan menyimpan data _session_ tersebut di dalam database sehingga server bisa mendapatkan _track_ tentang _session_ dari tiap user. ID dari _session_ tersebut juga akan disimpan dalam _cookies_. Selain untuk mempermudah proses autentikasi bagi _user_, cookies juga berperan dalam mendapatkan _track_ dari preferensi user dengan melacak pola aktivitas _user_ dalam aplikasi.

5. Berikut merupakan step-by-step implementasi Tugas 2:

### Membuat Fungsi Registrasi ####
Pertama-tama, aktifkan _virtual environment_ aplikasi terlebih dahulu. Lalu, masuklah ke `views.py` dan tambahkan _import_ `UserCreationForm` dari `django.contrib.auth.forms` serta `messages` dari `django.contrib`. Selanjutnya, buatlah fungsi register yang berfungsi untuk menampilkan formulir registrasi seperti di bawah ini:
```
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
```
Setelah itu, buatlah berkas `register.html` pada subdirektori `templates` yang berfungsi sebagai template dari laman registrasi (memuat form dengan method POST). Lalu, buatlah routing URL terhadap fungsi `register` pada berkas `urls.py` dengan meng-import `register` dari `main.views` dan menambahkan path berikut:
```
path('register/', register, name='register'),
```

### Membuat Fungsi Login ####
Bukalah berkas views.py dan tambahkan _import_ `authenticate` dan `login` dari `django.contrib.auth` serta `UserCreationForm` dan `AuthenticationForm` dari `django.contrib.auth.forms`. Selanjutnya, buatlah fungsi login_user seperti di bawah ini yang berfungsi untuk menampilkan laman login, mengautentikasi user, serta membuat _session_ baru untuk user:
```
def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:show_main')

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)
```
Setelah itu, buatlah berkas `login.html` pada subdirektori `templates` yang akan berperan sebagai template dari laman login (memuat formulir login dan tautan ke laman register untuk user yang belum memiliki akun). Lalu, buatlah routing URL terhadap fungsi `login_user` dengan meng-import fungsi tersebut dari `main.views` dan menambahkan _path_ berikut:
```
path('login/', login_user, name='login'),
```

### Membuat Fungsi Logout ####
Bukalah `views.py` lalu tambahkan _import_ `logout` dari `django.contrib.auth`. Selanjutnya, tambahkan fungsi `logout_user` seperti di bawah ini yang berfungsi untuk menjalankan proses logout bagi user dan memindahkan user kembali ke laman login:
```
def logout_user(request):
    logout(request)
    return redirect('main:login')
```
Setelah itu, bukalah berkas `main.html` dan tambahkan _button_ baru di bagian bawah template untuk melakukan logout:
```
<a href="{% url 'main:logout' %}">
  <button>Logout</button>
</a>
```
Kemudian, tambahkan routing URL terhadap fungsi `logout_user` pada `urls.py` dengan meng-_import_ fungsi tersebut dan menambahkan _path_ berikut:
```
path('logout/', logout_user, name='logout'),
```
Agar laman utama dari aplikasi hanya bisa dibuka oleh user yang sudah login, buatlah restriksi dengan pertama-tama meng-_import_ `login_required` dari `django.contrib.auth.decorators` pada berkas `views.py`. Kemudian, tambahkan kode `@login_required(login_url='/login')` di atas fungsi show_main untuk merestriksi akses laman utama khusus untuk user yang sudah login.

Setelah itu, lakukan sedikit pengujian dengan membuka server dan aplikasi. Lakukan register untuk membuat suatu akun baru dan cobalah untuk melakukan login dan logout dari akun tersebut.

### Implementasi Cookies ###
Bukalah kembali berkas `views.py` dan tambahkan import berupa `datetime`, `HttpResponseRedirect` dari `django.http`, serta `reverse` dari `django.urls`. Pada fungsi `login_user`, lakukan modifikasi pada blok `if form.is_valid():` untuk membuat _cookie_ baru yang menyimpan waktu login seperti berikut:
```
if form.is_valid():
    user = form.get_user()
    login(request, user)
    response = HttpResponseRedirect(reverse("main:show_main"))
    response.set_cookie('last_login', str(datetime.datetime.now()))
    return response
```
Kemudian, pada fungsi `show_main`, tambahkan kode `'last_login': request.COOKIES['last_login'],` di dalam `context` sehingga waktu login terakhir user (yang tersimpan dalam cookies) bisa dilihat di laman utama.

### Menghubungkan Model Product dengan User ###
Bukalah berkas `models.py` lalu tambahkan _import_ `User` dari `django.contrib.auth.models`. Lalu, pada class ShopEntry, tambahkan baris kode `user = models.ForeignKey(User, on_delete=models.CASCADE)` sehingga tiap model objek terhubung dengan suatu user. Kemudian, bukalah berkas views.py lalu dan lakukan modifikasi pada fungsi `create_shop_entry` sehingga menjadi seperti berikut:
```
def create_shop_entry(request):
    form = ShopEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        shop_entry = form.save(commit=False)
        shop_entry.user = request.user
        shop_entry.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "create_shop_entry.html", context)
```
Dengan ini, tiap entry baru yang dibuat dalam form akan terhubung dengan user yang membuatnya. Kemudian, ubahlah variabel `shop_entries` pada fungsi `show_main` menjadi seperti berikut:
```
shop_entries = ShopEntry.objects.filter(user=request.user)
```
Ubahlah juga nilai dari 'name' pada context menjadi seperti berikut:
```
'name': request.user.username,
```
Dengan ini, page utama akan menampilkan nama dari user yang sedang login serta entry-entry yang dibuat oleh user tersebut. Setelah itu, implementasikan perubahan pada model tadi dengan command `python manage.py makemigrations` dan `python manage.py migrate`. Terakhir, bukalah berkas `settings.py` dan tambahkan `import os`. Kemudian, ubahlah variabel DEBUG menjadi seperti berikut:
```
PRODUCTION = os.getenv("PRODUCTION", False)
DEBUG = not PRODUCTION
```
Setelah selesai, lakukan pengujian kembali dengan menjalankan server dan aplikasi. Buatlah registrasi terhadap akun kedua (yang berbeda dengan akun sebelumnya) dan lakukan login dengan akun tersebut. Cobalah untuk menambahkan beberapa entry baru pada akun tersebut, maka dapat dilihat bahwa entry yang dibuat hanya ditampilkan pada _session_ akun tersebut (begitu pula untuk entry yang dibuat pada akun pertama).