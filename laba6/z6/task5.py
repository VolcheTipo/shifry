from sdes import SDes


class SDesExtended(SDes):
    def F(self, block, k):
        exp = self.ep(block) ^ k
        l4, r4 = self.divide_into_two(exp, 8)
        return self.p4(self.mux(self.s0(l4), self.s1(r4), 2))

    def f_k(self, block, SK):
        l, r = self.divide_into_two(block, 8)
        return self.mux(l ^ self.F(r, SK), r, 4)

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
        #Шифрование одного байта с использованием уже вычисленных подключей
        if not (0 <= plaintext_block < 256):
            raise ValueError('plaintext_block must be a byte value (0..255)')
        return self.sdes(plaintext_block, self.k1, self.k2)

#запускь
if __name__ == '__main__':
    sdes = SDesExtended()
    key = int('0111111101', 2)
    sdes.key_schedule(key)
    plaintext = int('10101010', 2)
    cipher = sdes.encrypt(plaintext)
    print(f'plain = {bin(plaintext)[2:].zfill(8)}')
    print(f'cipher = {bin(cipher)[2:].zfill(8)}')
