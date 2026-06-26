#======================================================================
# Kelompok 14:
#
# Dafi Muzaki Wibisono      (J0403251155)
# Muhammad Taufan Noviandri (J0403251140)
# Aushaf Ghifary Aryanto    (J0403251123)
#
# Rute Kereta Api
#======================================================================

import os

# Konstanta lebar tampilan dipakai agar semua garis dan judul konsisten.
LEBAR_TAMPILAN = 60


def garis():
    print("=" * LEBAR_TAMPILAN)


def garis_tipis():
    print("-" * LEBAR_TAMPILAN)


def judul(teks, subteks=None):
    # Fungsi ini membuat tampilan judul program lebih rapi dan seragam.
    print()
    garis()
    print(teks.center(LEBAR_TAMPILAN))
    if subteks:
        print(subteks.center(LEBAR_TAMPILAN))
    garis()


def menu(teks, daftar_menu):
    # daftar_menu berisi pasangan nomor dan nama menu, sehingga menu mudah diubah.
    judul(teks)
    for nomor, nama_menu in daftar_menu:
        print(f"{nomor}. {nama_menu}")
    garis_tipis()


def pesan_sukses(teks):
    print(f"[OK] {teks}")


def pesan_info(teks):
    print(f"[INFO] {teks}")


def pesan_error(teks):
    print(f"[!] {teks}")


# Node menyimpan nama stasiun dan pointer ke node sebelum/sesudahnya.
class Node:
    def __init__(self, data):
        # data menyimpan nama stasiun, sedangkan next/prev menjadi penghubung rute.
        self.data = data
        self.next = None
        self.prev = None

# Doubly linked list digunakan untuk menyimpan urutan rute kereta.
class DoublyLinkedList:
    def __init__(self):
        # head menunjuk stasiun pertama, tail menunjuk stasiun terakhir.
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    # Menambahkan stasiun baru di awal rute.
    def insert_front(self, data):
        new_node = Node(data)
        if self.isEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    # Menambahkan stasiun baru di akhir rute.
    def insert_end(self, data):
        new_node = Node(data)
        if self.isEmpty():
            # Jika rute masih kosong, stasiun baru menjadi awal sekaligus akhir.
            self.head = new_node
            self.tail = new_node
        else:
            # Jika sudah ada data, stasiun baru disambungkan setelah tail lama.
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    # Menambahkan stasiun baru setelah stasiun tertentu.
    def insert_after(self, target, data):
        target_node = self.find_node(target)
        if not target_node:
            return False

        if target_node == self.tail:
            self.insert_end(data)
        else:
            new_node = Node(data)
            new_node.prev = target_node
            new_node.next = target_node.next
            target_node.next.prev = new_node
            target_node.next = new_node
            self.size += 1
        return True

    # Menghapus stasiun berdasarkan nama.
    def delete_station(self, key):
        target_node = self.find_node(key)
        if not target_node:
            return None

        deleted_data = target_node.data
        if self.head == self.tail:
            self.head = None
            self.tail = None
        elif target_node == self.head:
            self.head = self.head.next
            self.head.prev = None
        elif target_node == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            target_node.prev.next = target_node.next
            target_node.next.prev = target_node.prev

        self.size -= 1
        return deleted_data

    # Mencari node stasiun berdasarkan nama tanpa membedakan huruf besar/kecil.
    def find_node(self, key):
        # Pencarian dilakukan dari head sampai tail.
        temp = self.head
        while temp:
            if temp.data.lower() == key.lower():
                return temp
            temp = temp.next
        return None

    # Menampilkan daftar stasiun sesuai urutan rute asli dari file.
    def show_stations(self):
        if self.isEmpty():
            pesan_error("Rute kereta tidak tersedia!")
            return []

        # Data linked list diubah dulu menjadi list agar mudah diberi nomor urut.
        data = self.to_list()
        judul("DAFTAR STASIUN", "Sesuai urutan rute Bogor - Jakarta Kota")
        for nomor, stasiun in enumerate(data, start=1):
            print(f"| {nomor:>2}. {stasiun:<52} |")
        garis()
        return data

    # Mengubah input nomor/nama dari pengguna menjadi nama stasiun yang valid.
    def resolve_station_input(self, pilihan, daftar_stasiun):
        # Pengguna boleh memasukkan nomor stasiun sesuai daftar di menu 1.
        if pilihan.isdigit():
            nomor = int(pilihan)
            if 1 <= nomor <= len(daftar_stasiun):
                return daftar_stasiun[nomor - 1]
            return None

        # Jika bukan angka, input dianggap sebagai nama stasiun.
        node = self.find_node(pilihan)
        if node:
            return node.data
        return None

    # Mengambil potongan rute dari stasiun asal ke stasiun tujuan.
    def get_route_between(self, asal, tujuan):
        # Ambil node asal dan tujuan supaya rute bisa ditelusuri lewat pointer.
        node_asal = self.find_node(asal)
        node_tujuan = self.find_node(tujuan)

        if not node_asal or not node_tujuan:
            return None

        rute = []
        temp = node_asal
        # Coba telusuri ke depan, misalnya dari Bogor menuju Jakarta Kota.
        while temp:
            rute.append(temp.data)
            if temp == node_tujuan:
                return rute
            temp = temp.next

        rute = []
        temp = node_asal
        # Jika tidak ditemukan ke depan, telusuri ke belakang untuk arah sebaliknya.
        while temp:
            rute.append(temp.data)
            if temp == node_tujuan:
                return rute
            temp = temp.prev

        return None

    # Mengubah isi linked list menjadi list Python agar mudah diolah.
    def to_list(self):
        stasiun = []
        temp = self.head
        while temp:
            stasiun.append(temp.data)
            temp = temp.next
        return stasiun

    # Mengosongkan seluruh data rute.
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Menyimpan semua stasiun ke file teks.
    def save_file(self, filename="rute_kereta.txt"):
        try:
            # Setiap stasiun disimpan satu baris agar mudah dimuat kembali.
            with open(filename, "w") as f:
                temp = self.head
                while temp:
                    f.write(str(temp.data) + "\n")
                    temp = temp.next
            pesan_sukses(f"Data berhasil disimpan ke {filename}")
        except Exception as e:
            pesan_error(f"Gagal menyimpan data: {e}")

    # Memuat data stasiun dari file teks jika file tersedia.
    def load_file(self, filename="rute_kereta.txt"):
        # Bersihkan data lama agar isi linked list sama dengan isi file terbaru.
        self.clear()
        if not os.path.exists(filename):
            pesan_error("File data tidak ditemukan, memulai dengan rute kosong.")
            return
        
        try:
            with open(filename, "r") as f:
                for line in f:
                    stasiun = line.strip()
                    if stasiun:
                        # Setiap baris file dimasukkan lagi sebagai node baru.
                        self.insert_end(stasiun)
            pesan_sukses(f"Data berhasil dimuat dari {filename}")
        except Exception as e:
            pesan_error(f"Gagal memuat data: {e}")


def tambah_stasiun(dll):
    # Menambahkan stasiun baru dari input pengguna.
    stasiun = input("Masukkan nama stasiun: ").strip()
    if not stasiun:
        pesan_error("Nama stasiun tidak boleh kosong.")
        return
    if dll.find_node(stasiun):
        # Cegah nama stasiun ganda agar data rute tetap bersih.
        pesan_error(f"Stasiun {stasiun} sudah ada dalam rute.")
        return

    menu("POSISI TAMBAH STASIUN", [
        ("1", "Awal rute"),
        ("2", "Setelah stasiun tertentu"),
        ("3", "Akhir rute"),
    ])
    posisi = input("Pilih posisi [1-3]: ").strip()

    if posisi == "1":
        dll.insert_front(stasiun)
        pesan_sukses(f"Stasiun {stasiun} berhasil ditambahkan di awal rute.")
    elif posisi == "2":
        # Tampilkan daftar agar pengguna bisa memilih posisi penyisipan.
        daftar_stasiun = dll.show_stations()
        target_input = input("Tambahkan setelah stasiun (nama/nomor): ").strip()
        target = dll.resolve_station_input(target_input, daftar_stasiun)
        if not target:
            pesan_error("Stasiun tujuan penyisipan tidak ditemukan.")
            return
        dll.insert_after(target, stasiun)
        pesan_sukses(f"Stasiun {stasiun} berhasil ditambahkan setelah {target}.")
    elif posisi == "3":
        dll.insert_end(stasiun)
        pesan_sukses(f"Stasiun {stasiun} berhasil ditambahkan di akhir rute.")
    else:
        pesan_error("Pilihan posisi tidak valid.")
        return

    # File disimpan satu kali setelah proses tambah benar-benar berhasil.
    dll.save_file()


def hapus_stasiun(dll):
    # Menghapus stasiun berdasarkan pilihan nama atau nomor.
    if dll.isEmpty():
        pesan_error("Tidak ada stasiun yang tersedia!")
        return

    # Tampilkan daftar agar pengguna bisa memilih stasiun yang akan dihapus.
    daftar_stasiun = dll.show_stations()
    hapus_input = input("Hapus stasiun (nama/nomor): ").strip()
    stasiun_hapus = dll.resolve_station_input(hapus_input, daftar_stasiun)

    if not stasiun_hapus:
        pesan_error("Stasiun yang ingin dihapus tidak ditemukan.")
        return

    konfirmasi = input(f"Yakin hapus stasiun {stasiun_hapus}? (y/n): ").strip().lower()
    if konfirmasi != "y":
        pesan_info("Hapus stasiun dibatalkan.")
        return

    deleted_data = dll.delete_station(stasiun_hapus)
    if deleted_data:
        pesan_sukses(f"Stasiun {deleted_data} berhasil dihapus.")
        dll.save_file()


def main():
    dll = DoublyLinkedList()

    # Rute dimuat otomatis dari file teks saat program pertama dijalankan.
    dll.load_file()

    # Loop menu utama akan berjalan sampai pengguna memilih keluar.
    while True:
        menu("SISTEM RUTE KRL RED LINE", [
            ("1", "Tampilkan data stasiun"),
            ("2", "Tentukan rute perjalanan"),
            ("3", "Kelola stasiun"),
            ("4", "Keluar"),
        ])
        print(f"Jumlah stasiun aktif: {dll.size}")

        pilihan = input("Pilih menu [1-4]: ").strip()

        if pilihan == "1":
            # Menu 1 hanya bertugas menampilkan daftar stasiun lengkap.
            dll.show_stations()

        elif pilihan == "2":
            # Menentukan rute berdasarkan pilihan stasiun asal dan tujuan.
            if dll.isEmpty():
                pesan_error("Rute kereta tidak tersedia!")
                continue

            # Tampilkan daftar agar pengguna bisa memilih stasiun berdasarkan nama atau nomor.
            daftar_stasiun = dll.show_stations()
            asal_input = input("\nDari stasiun (nama/nomor): ").strip()
            tujuan_input = input("Ke stasiun (nama/nomor): ").strip()
            asal = dll.resolve_station_input(asal_input, daftar_stasiun)
            tujuan = dll.resolve_station_input(tujuan_input, daftar_stasiun)

            if not asal_input or not tujuan_input:
                # Validasi agar proses pencarian rute tidak memakai input kosong.
                pesan_error("Stasiun asal dan tujuan tidak boleh kosong.")
            elif not asal or not tujuan:
                pesan_error("Stasiun asal atau tujuan tidak ditemukan dalam rute.")
            elif asal.lower() == tujuan.lower():
                pesan_error("Stasiun asal dan tujuan tidak boleh sama.")
            else:
                rute_perjalanan = dll.get_route_between(asal, tujuan)
                if rute_perjalanan:
                    # Rute yang ditemukan ditampilkan beserta ringkasan jumlah stasiun.
                    judul("RUTE PERJALANAN", f"{asal} menuju {tujuan}")
                    pesan_info(f"Arah perjalanan: {asal} menuju {tujuan}")
                    print(" -> ".join(rute_perjalanan))
                    garis_tipis()
                    pesan_info(f"Jumlah stasiun yang dilewati: {len(rute_perjalanan)}")
                    pesan_info(f"Jumlah perpindahan antarstasiun: {len(rute_perjalanan) - 1}")
                else:
                    pesan_error("Rute perjalanan tidak dapat ditemukan.")

        elif pilihan == "3":
            menu("KELOLA STASIUN", [
                ("1", "Tambah stasiun"),
                ("2", "Hapus stasiun"),
                ("3", "Kembali"),
            ])
            pilihan_kelola = input("Pilih menu kelola [1-3]: ").strip()

            if pilihan_kelola == "1":
                tambah_stasiun(dll)
            elif pilihan_kelola == "2":
                hapus_stasiun(dll)
            elif pilihan_kelola == "3":
                pesan_info("Kembali ke menu utama.")
            else:
                pesan_error("Pilihan kelola tidak valid.")

        elif pilihan == "4":
            judul("TERIMA KASIH", "Program Rute Kereta Api selesai")
            break

        else:
            pesan_error("Pilihan tidak valid. Silakan pilih menu 1-4.")


if __name__ == "__main__":
    main()
