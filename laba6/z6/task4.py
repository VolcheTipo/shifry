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
        #Один раунд сети Фейстеля: 8-битный блок, 8-битный подключ -> 8-битный блок
        l, r = self.divide_into_two(block, 8)
        f_res = self.F(r, SK)
        new_l = l ^ f_res
        # В S-DES: (L XOR F) || R
        return self.mux(new_l, r, 4)

    def sdes(self, block, k1, k2):
        #Полный цикл шифрования S-DES
        step1 = self.ip(block)
        print(f"After IP: {bin(step1)[2:].zfill(8)}")
        step2 = self.f_k(step1, k1)
        print(f"After f_k: {bin(step2)[2:].zfill(8)}")
        step3 = self.sw(step2)
        print(f"After SW: {bin(step3)[2:].zfill(8)}")
        step4 = self.f_k(step3, k2)
        print(f"After f_k: {bin(step4)[2:].zfill(8)}")
        step5 = self.ipinv(step4)
        print(f"After IPinv: {bin(step5)[2:].zfill(8)}")
        return step5

#запускь
if __name__ == "__main__":
    sdes = SDesExtended()
    block = int('11101010', 2)
    k1 = int('01011111', 2)
    k2 = int('11111100', 2)
    print(f"block: {bin(block)[2:].zfill(8)}")
    print(f"K1: {bin(k1)[2:].zfill(8)}   K2: {bin(k2)[2:].zfill(8)}")
    res = sdes.sdes(block, k1, k2)