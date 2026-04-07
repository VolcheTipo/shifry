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
        print(f"L: {bin(l)[2:].zfill(4)}   R: {bin(r)[2:].zfill(4)}")

        f_res = self.F(r, SK)
        print(f"F(R, SK): {bin(f_res)[2:].zfill(4)}")

        new_r = l ^ f_res
        print(f"L xor F(R, K): {bin(new_r)[2:].zfill(4)}")

        # В S-DES порядок: (L XOR F) || R
        result = self.mux(new_r, r, 4)  # new_r идет первым!
        print(f"return: {bin(result)[2:].zfill(8)}")

        return result

#запускь
if __name__ == "__main__":
    sdes = SDesExtended()
    block = int('10110011', 2)
    sk = int('01011111', 2)
    print(f"block: {bin(block)[2:].zfill(8)}")
    print(f"SK: {bin(sk)[2:].zfill(8)}")
    res = sdes.f_k(block, sk)