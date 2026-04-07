from sdes import SDes


class SDesExtended(SDes):
    def F(self, block, k):
        exp_block = self.ep(block) ^ k
        l4, r4 = self.divide_into_two(exp_block, 8)
        return self.p4(self.mux(self.s0(l4), self.s1(r4), 2))

    def f_k(self, block, SK):
        #Один раунд сети Фейстеля
        l, r = self.divide_into_two(block, 8)
        f_res = self.F(r, SK)
        new_l = l ^ f_res
        # ВАЖНО: сначала (L XOR F), потом R
        return self.mux(new_l, r, 4)

    def sdes(self, block, k1, k2):
        return self.ipinv(self.f_k(self.sw(self.f_k(self.ip(block), k1)), k2))

    def key_schedule(self, key):
        k = self.p10(key)
        l, r = self.divide_into_two(k, 10)
        l1, r1 = self.ls1(l), self.ls1(r)
        self.k1 = self.p8(self.mux(l1, r1, 5))
        l2, r2 = self.ls2(l1), self.ls2(r1)
        self.k2 = self.p8(self.mux(l2, r2, 5))
        return self.k1, self.k2

    def encrypt(self, plaintext_block):
        return self.sdes(plaintext_block, self.k1, self.k2)

    def decrypt(self, ciphertext_block):
        #Расшифрование: ключи в обратном порядке!
        return self.sdes(ciphertext_block, self.k2, self.k1)

#запускь 
if __name__ == "__main__":
    sdes = SDesExtended()
    key = int('0111111101', 2)
    sdes.key_schedule(key)
    original = int('10101010', 2)
    print(f"Исходный:  {bin(original)[2:].zfill(8)}")
    ct = sdes.encrypt(original)
    print(f"Зашифровано: {bin(ct)[2:].zfill(8)}")
    pt = sdes.decrypt(ct)
    print(f"Расшифровка: {bin(pt)[2:].zfill(8)}")
    if pt == original:
        print("Успешно, расшифровка совпадает с исходным")
    else:
        print("Ошибка, расшифровка НЕ совпадает с исходным")