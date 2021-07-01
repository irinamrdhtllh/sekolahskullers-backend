# sekolahskullers-backend

Server backend penyedia data melalui REST API untuk website Sekolah Skullers 2021.

## Prosedur instalasi

Clone repository ini.

    $ git clone https://github.com/irinamrdhtllh/sekolahskullers-backend.git

Buat dan aktifkan virtual environment Python baru.

    $ python -m venv .venv
    $ .venv\Scripts\activate.bat

Jika berhasil maka akan muncul `$ (.venv)` di sebelah kiri terminal.

Install seluruh package yang diperlukan.

    $ (.venv) pip install -r requirements.txt

## Penggunaan laman admin

Terdapat laman admin yang dapat digunakan untuk meninjau dan mengubah secara manual seluruh data yang tersedia. Untuk mengaksesnya diperlukan akun admin yang dapat dibuat menggunakan perintah berikut.

    $ (env) python manage.py createsuperuser

Jalankan server

    $ (.venv) python manage.py runserver

Laman admin dapat diakses pada alamat `/admin`