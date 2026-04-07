from sdes import SDes


class SDesExtended(SDes):
    def key_schedule(self, key):
        #Алгоритм расширения ключа. Формирует k1 и k2 из 10-битного key
        # 1. Применяем P10
        k_p10 = self.p10(key)
        print(f"After P10: {bin(k_p10)[2:].zfill(10)}")

        # 2. Разделяем на две 5-битные части
        l, r = self.divide_into_two(k_p10, 10)

        # 3. Циклический сдвиг LS1
        l1 = self.ls1(l)
        r1 = self.ls1(r)
        print(f"After LS-1: {bin(l1)[2:].zfill(5)} {bin(r1)[2:].zfill(5)}")

        # 4. Объединяем и применяем P8 -> K1
        k1_in = self.mux(l1, r1, 5)
        self.k1 = self.p8(k1_in)
        print(f"After P8 (K1): {bin(self.k1)[2:].zfill(8)}")

        # 5. Циклический сдвиг LS2
        l2 = self.ls2(l1)
        r2 = self.ls2(r1)
        print(f"After LS-2: {bin(l2)[2:].zfill(5)} {bin(r2)[2:].zfill(5)}")

        # 6. Объединяем и применяем P8 -> K2
        k2_in = self.mux(l2, r2, 5)
        self.k2 = self.p8(k2_in)
        print(f"After P8 (K2): {bin(self.k2)[2:].zfill(8)}")

        return self.k1, self.k2


# запускь
if __name__ == "__main__":
    sdes = SDesExtended()
    key = int('0111111101', 2)
    print(f"Key: {bin(key)[2:].zfill(10)}\n")
    k1, k2 = sdes.key_schedule(key)
    print(f"\nK1: {bin(k1)[2:].zfill(8)}")
    print(f"K2: {bin(k2)[2:].zfill(8)}")