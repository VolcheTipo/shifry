from sdes import SDes


class SDesExtended(SDes):
    def F(self, block, k):
        #4-битный блок, 8-битный ключ -> 4-битный выход
        # Расширение 4 бит до 8 бит
        exp_block = self.ep(block)
        print(f"After E/P: {bin(exp_block)[2:].zfill(8)}")

        # XOR с раундовым ключом
        xored = exp_block ^ k
        print(f"After xor with subkey: {bin(xored)[2:].zfill(8)}")

        # Разделяем на две 4-битные половины
        left4, right4 = self.divide_into_two(xored, 8)

        # Подстановка через S-боксы
        s0_out = self.s0(left4)  # 2 бита
        print(f"After S0: {bin(s0_out)[2:].zfill(2)}")

        s1_out = self.s1(right4)  # 2 бита
        print(f"After S1: {bin(s1_out)[2:].zfill(2)}")

        # Конкатенация и финальная перестановка P4
        combined = self.mux(s0_out, s1_out, 2)
        result = self.p4(combined)
        print(f"After P4: {bin(result)[2:].zfill(4)}")
        return result

# запускь
if __name__ == "__main__":
    sdes = SDesExtended()
    block = int('0011', 2)
    k = int('01011111', 2)
    print(f"Input block: {bin(block)[2:].zfill(4)}")
    print(f"Subkey: {bin(k)[2:].zfill(8)}\n")
    res = sdes.F(block, k)
    print(f"\nResult: {bin(res)[2:].zfill(4)}")