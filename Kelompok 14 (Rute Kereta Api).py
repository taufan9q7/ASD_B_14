import os

# Node menyimpan nama stasiun dan pointer ke node sebelum/sesudahnya.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Doubly linked list digunakan untuk menyimpan urutan rute kereta.
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    # Menambahkan stasiun baru di akhir rute.
    def push(self, data):
        new_node = Node(data)
        if self.isEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    # Menghapus stasiun terakhir dari rute.
    def pop(self):
        if self.isEmpty():
            print("Tidak ada stasiun yang tersedia!")
            return None
        popData = self.tail.data
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        print(f"Rute ke stasiun {popData} telah dihapus.")
        self.size -=1
        return popData

    # Menampilkan rute dari stasiun pertama sampai terakhir.
    def traverse_depan(self):
        if self.isEmpty():
            print("Rute kereta tidak tersedia!")
            return False
        print("\nPindah stasiun:")
        stasiun = []
        temp = self.head
        while temp:
            stasiun.append(str(temp.data))
            temp = temp.next
        print(" -> ".join(stasiun))

    # Menampilkan rute dari stasiun terakhir sampai pertama.
    def traverse_belakang(self):
        if self.isEmpty():
            print("Rute kereta tidak tersedia!")
            return False
        print("\nPindah stasiun:")
        stasiun = []
        temp = self.tail
        while temp:
            stasiun.append(str(temp.data))
            temp = temp.prev
        print(" -> ".join(stasiun))

    # Mencari stasiun berdasarkan nama tanpa membedakan huruf besar/kecil.
    def search(self, key):
        if self.isEmpty():
            print("Stasiun kereta ini tidak tersedia!")
            return False
        temp = self.head 
        while temp:
            if temp.data.lower() == key.lower():
                print(f"Stasiun {key} ditemukan.")
                return True 
            temp = temp.next
        print(f"Stasiun {key} tidak ditemukan.") 
        return False

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

    # Mengurutkan rute berdasarkan abjad, lalu memasukkan kembali ke linked list.
    def sort(self, ascending=True):
        if self.isEmpty():
            print("Rute kereta tidak tersedia!")
            return False

        data = sorted(self.to_list(), key=str.lower, reverse=not ascending)
        self.clear()
        for stasiun in data:
            self.push(stasiun)

        urutan = "A-Z" if ascending else "Z-A"
        print(f"Rute berhasil diurutkan ({urutan}).")
        return True
    
    # Menyimpan semua stasiun ke file teks.
    def save_file(self, filename="rute_kereta.txt"):
        try:
            with open(filename, "w") as f:
                temp = self.head
                while temp:
                    f.write(str(temp.data) + "\n")
                    temp = temp.next
            print(f"Data berhasil disimpan ke {filename}")
        except Exception as e:
            print(f"Gagal menyimpan data: {e}")

    # Memuat data stasiun dari file teks jika file tersedia.
    def load_file(self, filename="rute_kereta.txt"):
        if not os.path.exists(filename):
            print("File data tidak ditemukan, memulai dengan rute kosong.")
            return
        
        try:
            with open(filename, "r") as f:
                for line in f:
                    stasiun = line.strip()
                    if stasiun:
                        self.push(stasiun)
            print(f"Data berhasil dimuat dari {filename}")
        except Exception as e:
            print(f"Gagal memuat data: {e}")

def main():
    dll = DoublyLinkedList()

    # Data lama dimuat otomatis saat program pertama dijalankan.
    dll.load_file()

    # Loop menu utama akan berjalan sampai pengguna memilih keluar.
    while True:
        print("\n=== Rute Kereta Api ===")
        print(f"Jumlah stasiun: {dll.size}")
        print("1. Tambah stasiun")
        print("2. Hapus stasiun")
        print("3. Tampilkan rute dari depan")
        print("4. Tampilkan rute dari belakang")
        print("5. Cari stasiun")
        print("6. Sorting rute")
        print("7. Simpan data")
        print("8. Muat ulang data")
        print("9. Keluar")
        print("========================")

        pilihan = input("Pilih menu (1-9): ").strip()

        if pilihan == "1":
            # Menambahkan stasiun baru dari input pengguna.
            stasiun = input("Masukkan nama stasiun: ").strip()
            if stasiun:
                dll.push(stasiun)
                print(f"Stasiun {stasiun} berhasil ditambahkan.")
            else:
                print("Nama stasiun tidak boleh kosong.")

        elif pilihan == "2":
            # Menghapus stasiun paling akhir.
            dll.pop()

        elif pilihan == "3":
            dll.traverse_depan()

        elif pilihan == "4":
            dll.traverse_belakang()

        elif pilihan == "5":
            key = input("Masukkan nama stasiun yang dicari: ").strip()
            if key:
                dll.search(key)
            else:
                print("Nama stasiun tidak boleh kosong.")

        elif pilihan == "6":
            # Submenu untuk memilih jenis pengurutan.
            print("\n=== Sorting Rute ===")
            print("1. Urutkan A-Z")
            print("2. Urutkan Z-A")
            print("3. Kembali")
            pilihan_sort = input("Pilih sorting (1-3): ").strip()

            if pilihan_sort == "1":
                dll.sort(ascending=True)
                dll.traverse_depan()
            elif pilihan_sort == "2":
                dll.sort(ascending=False)
                dll.traverse_depan()
            elif pilihan_sort == "3":
                print("Kembali ke menu utama.")
            else:
                print("Pilihan sorting tidak valid.")

        elif pilihan == "7":
            dll.save_file()

        elif pilihan == "8":
            dll.clear()
            dll.load_file()

        elif pilihan == "9":
            # Pengguna dapat menyimpan perubahan sebelum program ditutup.
            simpan = input("Simpan data sebelum keluar? (y/n): ").strip().lower()
            if simpan == "y":
                dll.save_file()
            print("Terima kasih telah menggunakan program Rute Kereta Api.")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih menu 1-9.")


if __name__ == "__main__":
    main()
