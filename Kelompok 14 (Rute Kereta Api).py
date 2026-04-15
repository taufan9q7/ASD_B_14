import os

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

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

    def search(self, key):
        if self.isEmpty():
            print("Stasiun kereta ini tidak tersedia!")
            return False
        temp = self.head 
        while temp:
            if temp.data == key:
                print(f"Stasiun {key} ditemukan.")
                return True 
            temp = temp.next
        print(f"Stasiun {key} tidak ditemukan.") 
        return False
    
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
    while True:
        print("=== Rute Kereta Api ===")
        print("1. Tambah stasiun")
        print("2. Hapus stasiun")
        print("3. ")
        print("=== Rute Kereta Api ===")
        
