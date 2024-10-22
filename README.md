# TUGAS 2 - TRANSFER STRING TERENKRIPSI ANTAR USER DENGAN SOCKET
README ini berisikan penjelasan mengenai kode yang telah dibuat `socket_server.py` & `socket_client.py`

## ANGGOTA
<div align="center">
  
| Nama                     | NRP          |
|--------------------------|--------------|
| Vidiawan Nabiel Arrasyid | 5025221231   |

</div>


## DAFTAR ISI
- [Anggota](#anggota)
- [Daftar Isi](#daftar-isi)
- [Soal](#soal)
- [1. Server Socket](#1-server-socket)
  - [1.1 Import](#11-import)
  - [1.2 Deklarasi Key, Host, dan Port](#12-deklarasi-key-host-dan-port)
  - [1.3 Inisialisasi Socket](#13-inisialisasi-socket)
  - [1.4 Komunikasi & Alamat](#14-komunikasi--alamat)
  - [1.5 Menerima Pesan](#15-menerima-pesan)
  - [1.6 Dekripsi](#16-dekripsi)
  - [1.7 Menerima Input User](#17-menerima-input-user)
  - [1.8 Mengirim Pesan](#18-mengirim-pesan)
  - [1.9 Menutup Koneksi](#19-menutup-koneksi)
- [2. Client Socket](#2-client-socket)
  - [2.1 Inisialisasi Socket](#21-inisialisasi-socket)
  - [2.2 Menerima Input User](#22-menerima-input-user)
  - [2.3 Mengirim Pesan](#23-mengirim-pesan)
  - [2.4 Menerima Pesan](#24-menerima-pesan)
  - [2.5 Dekripsi](#25-dekripsi)
- [3. Penggunaan](#3-penggunaan)
  - [3.1 Buka Dua Terminal](#31-buka-dua-terminal)
  - [3.2 Jalankan File `socket_server.py` di Salah Satu Terminal](#32-jalankan-file-socket_serverpy-di-salah-satu-terminal)
  - [3.3 Jalankan File `socket_client.py` di Terminal Lainnya](#33-jalankan-file-socket_clientpy-di-terminal-lainnya)
  - [3.4 Kirim Pesan Melalui Client](#34-kirim-pesan-melalui-client)
  - [3.5 Kirim Pesan Melalui Server](#35-kirim-pesan-melalui-server)
- [4. Sumber](#4-sumber)
  - [4.1 Penggunaan Socket dengan Python [Digital Ocean]](#41-penggunaan-socket-dengan-python-digital-ocean)

## Soal
Pengembangan program enkripsi dan dekripsi DES dari Tugas 1:
1. Implementasi transfer string terenkripsi antar 2 user menggunakan socket programming (penerima dapat mendekripsi string dari pengirim)
2. Enkripsi dan Dekripsi harus bisa menerima input lebih dari 64bit (8 karakter)
3. String enkripsi wajib dikirimkan melalui socket (tidak boleh read/write file)
4. Untuk key dianggap kedua client tau (boleh hardcode)


## 1 SERVER SOCKET
Penjelasan mengenai `socket_server.py`

#### 1.1 IMPORT
Pertama kita import `socket` untuk membuat koneksi serta `encrypt` dan `decrypt` dari `des_tugas1` sebagai algoritma enkripsi dan dekripsi DES dari tugas pertama 
```py
import socket
from des_tugas1 import encrypt, decrypt
```

#### 1.2 DEKLARASI KEY, HOST, DAN PORT
Kemudian kita deklarasikan `key` yang akan digunakan untuk enkripsi dan dekripsi, `host`, serta `port` yang akan digunakan untuk koneksi
```py
SHARED_KEY = "password"
    
host = '127.0.0.1'
port = 5000
```
Kita atur `host` -> `localhost` sehingga hanya bisa diakses di komputer yang sama dan `port` -> `5000` 

#### 1.3 INISIALISASI SOCKET
Inisialisasikan socket baru dengan nama `server_socket`
```py
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together

# configure how many clients the server can listen simultaneously
server_socket.listen(1)
```
buat agar `server_socket` mendengarkan ke `host` dan `port` yang sudah diatur dan hanya menerima satu `client`

#### 1.4 KOMUNIKASI & ALAMAT
Buat variabel `conn` yang akan digunakan untuk berkomunikasi dan `address` untuk menyimpan alamat dari `client` yang terhubung
```py
conn, address = server_socket.accept()  # accept new connection
```

#### 1.5 MENERIMA PESAN
Buat variable `encrypted_data` yang akan menerima data dari `client`
```py
while True:
    # receive data stream. It won't accept data packet greater than 1024 bytes
    encrypted_data = conn.recv(1024).decode()
    if not encrypted_data:
        # if no data is received, break
        break
```
`server` akan terus menerima/mengirim data dari/ke `client` hingga tidak ada data yang diterima

#### 1.6 DEKRIPSI
Kita akan menggunakan try & except block untuk mencoba mendekripsi data yang dikirim oleh `client`
```py
try:
    decrypted_data = decrypt(encrypted_data, SHARED_KEY)
    print("\nReceived message:", encrypted_data)
    print("\nDecrypted message:", decrypted_data)
except Exception as e:
    print("Error decrypting message:", str(e))
    decrypted_data = "Error decrypting message"
```
`decrypted_data` akan ditampilkan dan jika ada error akan di lempar ke exception block untuk menyampaikan pesan error

#### 1.7 MENERIMA INPUT USER
Secara bergantian dengan `client`, `server` dapat menerima input dari `user` yang akan dikirim pada `client`
```py
data = input('\n -> ')
    if data.lower().strip() == 'bye':
        break
```
jika `user` memberikan input _bye_ maka `server` akan berhenti menerima pesan

#### 1.8 MENGIRIM PESAN
Kita kembali menggunakan try & except block dimana `server` akan mencoba untuk mengenkripsi data yang diberikan oleh `user` dan mengirimnya ke `client`
```py
try:
    encrypted_data = encrypt(data, SHARED_KEY)
    conn.send(encrypted_data.encode())  # send data to the client
except Exception as e:
    print("Error encrypting message:", str(e))
    conn.send("Error encrypting message".encode())
```
jika terjadi kesalahan maka akan dilempar ke exception block untuk menampilkan pesan error dan mengirimkan pesan error ke `client`

#### 1.9 MENUTUP KONEKSI
Ketika sudah selesai `server` akan menutup koneksi
```py
conn.close()  # close the connection
```


## 2 CLIENT SOCKET
Penjelasan mengenai `socket_client.py`. `socket_client.py` memiliki import, deklarasi `key`, `host`, dan `port` yang sama dengan `socket_server.py` karena akan terhubung dengan `socket_server.py`

#### 2.1 INISIALISASI SOCKET
Inisialisasikan socket baru dengan nama `client_socket` kemudian melakukan koneksi ke `server`
```py
client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server
```

#### 2.2 MENERIMA INPUT USER
Deklarasikan variabel `data` untuk menerima input dari `user`
```py
data = input('\n -> ')  # take input
```

#### 2.3 MENGIRIM PESAN
`client` akan menggunakan try & except block untuk menccoba mengenkripsi data dan mengirimkannya ke `server`
```py
while data.lower().strip() != 'bye':
    try:
        encrypted_data = encrypt(data, SHARED_KEY)
        client_socket.send(encrypted_data.encode())  # send message
        print("Sent encrypted message:", encrypted_data) 
    except Exception as e:
        print("Error encrypting message:", str(e))
        client_socket.send("Error encrypting message".encode())
```
`client` akan terus menerima/mengirim data dari/ke `server` hingga `user` menginputkan _bye_. Jika terjadi kesalahan dalam enkripsi atau pengiriman pesan maka akan dilempar ke except block untuk menyampaikan pesan error dan mengirimnya ke `server`

#### 2.4 MENERIMA PESAN
Inisialisasi variabel `encrypted_data` untuk menerima data dari `server`
```py
encrypted_data = client_socket.recv(1024).decode()  # receive response
```

#### 2.5 DEKRIPSI
Kita akan menggunakan try & except block untuk mencoba mendekripsi data yang dikirim oleh `server`, kemudian pesan akan ditampilkan
```py
try:
    decrypted_data = decrypt(encrypted_data, SHARED_KEY)
    print("\nReceived message:", encrypted_data)  # show in terminal
    print("\nDecrypted message:", decrypted_data)
except Exception as e:
    print("Error decrypting message:", str(e))
    decrypted_data = "Error decrypting message"
```
`decrypted_data` akan ditampilkan dan jika ada error akan di lempar ke exception block untuk menyampaikan pesan error

#### 2.6 MENUTUP KONEKSI
Ketika sudah selesai `client` akan menutup koneksi
```py
client_socket.close()  # close the connection
```


## 3 PENGGUNAAN
#### 3.1 BUKA DUA TERMINAL
![buka-terminal](https://github.com/nabielvna/KI-B-231/blob/tugas2/Assets/buka-terminal.png?raw=true)
#### 3.2 JALANKAN FILE `socket_server.py` DI SALAH SATU TERMINAL
![jalankan-server](https://github.com/nabielvna/KI-B-231/blob/tugas2/Assets/jalankan-server.png?raw=true)
**Windows**
```
python socket_server.py
```
kemudian tunggu hingga `client` dijalankan

#### 3.3 JALANKAN FILE `socket_client.py` DI TERMINAL LAINNYA
![jalankan-client](https://github.com/nabielvna/KI-B-231/blob/tugas2/Assets/jalankan-client.png?raw=true)
**Windows**
```
python socket_client.py
```
#### 3.4 KIRIM PESAN MELALUI CLIENT
![kirim-pesan-melalui-client](https://github.com/nabielvna/KI-B-231/blob/tugas2/Assets/kirim-pesan-melalui-client.png?raw=true)

#### 3.5 KIRIM PESAN MELALUI SERVER
![kirim-pesan-melalui-server](https://github.com/nabielvna/KI-B-231/blob/tugas2/Assets/kirim-pesan-melalui-server.png?raw=true)


## 4 SUMBER
#### 4.1 Penggunaan socket dengan python [Digital Ocean](https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client)
