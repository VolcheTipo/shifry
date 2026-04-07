from sdes import SDes


class SDesExtended(SDes):
    def F(self, block, k):
        #4-битный блок, 8-битный ключ -> 4-битный выход
        exp_block = self.ep(block)
        xored = exp_block ^ k
        left4, right4 = self.divide_into_two(xored, 8)
        s0_out = self.s0(left4)
        s1_out = self.s1(right4)
        combined = self.mux(s0_out, s1_out, 2)
        return self.p4(combined)

    def f_k(self, block, SK):
        #Один раунд сети Фейстеля
        l, r = self.divide_into_two(block, 8)
        f_res = self.F(r, SK)
        new_l = l ^ f_res
        # ВАЖНО: (L XOR F) || R
        return self.mux(new_l, r, 4)

    def sdes(self, block, k1, k2):
        #Полный цикл шифрования S-DES
        step1 = self.ip(block)
        step2 = self.f_k(step1, k1)
        step3 = self.sw(step2)
        step4 = self.f_k(step3, k2)
        step5 = self.ipinv(step4)
        return step5

    def key_schedule(self, key):
        #Алгоритм расширения ключа
        k = self.p10(key)
        l, r = self.divide_into_two(k, 10)
        l1, r1 = self.ls1(l), self.ls1(r)
        self.k1 = self.p8(self.mux(l1, r1, 5))
        l2, r2 = self.ls2(l1), self.ls2(r1)
        self.k2 = self.p8(self.mux(l2, r2, 5))
        return self.k1, self.k2

    def encrypt(self, plaintext_block):
        #Шифрование одного байта
        return self.sdes(plaintext_block, self.k1, self.k2)

    def decrypt(self, ciphertext_block):
        #Расшифрование одного байта
        return self.sdes(ciphertext_block, self.k2, self.k1)

    def encrypt_data(self, data):
        #Шифрование массива байт
        return [self.encrypt(b) for b in data]

    def decrypt_data(self, data):
        #Расшифрование массива байт
        return [self.decrypt(b) for b in data]

#запускь
if __name__ == "__main__":
    sdes = SDesExtended()
    key = int('0111111101', 2)  # 509 в десятичной
    sdes.key_schedule(key)
    print(f"Ключ: {bin(key)[2:].zfill(10)}")
    print(f"K1: {bin(sdes.k1)[2:].zfill(8)}")
    print(f"K2: {bin(sdes.k2)[2:].zfill(8)}\n")
    plaintext = [234, 54, 135, 98, 47]
    print(f"Открытый текст: {plaintext}")
    ciphertext = sdes.encrypt_data(plaintext)
    print(f"Зашифрованный текст: {ciphertext}")
    print(f"Ожидаемый результат: [162, 222, 0, 10, 83]")
    decrypted = sdes.decrypt_data(ciphertext)
    print(f"Расшифрованный текст: {decrypted}")
    if ciphertext == [162, 222, 0, 10, 83]:
        print("\nУспешно, результат совпадает с ожидаемым")
    else:
        print("\nОшибка, результат НЕ совпадает с ожидаемым.")
    if decrypted == plaintext:
        print("Расшифровка верна")
    else:
        print("Расшифровка неверна")