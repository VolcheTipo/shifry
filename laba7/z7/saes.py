import numpy as np


class SAES():
    S_Box = np.array([['9', '4', 'a', 'b'], ['d', '1', '8', '5'], ['6', '2', '0', '3'], ['c', 'e', 'f', '7']])
    S_InvBox = np.array([['a', '5', '9', 'b'], ['1', '7', '8', 'f'], ['6', '0', '2', '3'], ['c', '4', 'd', 'e']])
    RCON1 = int('10000000', 2)
    RCON2 = int('00110000', 2)
    modulus = int('10011', 2)
    column_Matrix = list([['1', '4'], ['4', '1']])
    column_InvMatrix = list([['9', '2'], ['2', '9']])
    state_matrix = []

    def __init__(self, column_Matrix, modulus):
        """
        раундовые ключи. рассчитываются в функции key_schedule
        """

        self.column_Matrix = column_Matrix
        self.modulus = modulus
        _, self.RCON1 = self.gf_divide(int('01000', 2), modulus)
        _, self.RCON2 = self.gf_divide(int('10000', 2), modulus)
        self.RCON1 *= 16
        self.RCON2 *= 16
        self.find_inverse_matrix()

    def find_inverse_matrix(self):
        a = int(self.column_Matrix[0][0], 16)
        b = int(self.column_Matrix[0][1], 16)
        c = int(self.column_Matrix[1][0], 16)
        d = int(self.column_Matrix[1][1], 16)


        ad = self.gf_multiply_modular(a, d, self.modulus, 4)
        bc = self.gf_multiply_modular(b, c, self.modulus, 4)
        det = ad ^ bc
        det_inv = self.gf_mi(det, self.modulus, 4)


        self.column_InvMatrix[0][0] = hex(self.gf_multiply_modular(det_inv, d, self.modulus, 4))[2:]
        self.column_InvMatrix[0][1] = hex(self.gf_multiply_modular(det_inv, b, self.modulus, 4))[2:]
        self.column_InvMatrix[1][0] = hex(self.gf_multiply_modular(det_inv, c, self.modulus, 4))[2:]
        self.column_InvMatrix[1][1] = hex(self.gf_multiply_modular(det_inv, a, self.modulus, 4))[2:]


    def divide_into_two(self, k, n):
        """
        функция разделяет n-битовое число k на два (n/2)-битовых числа
        """
        n2 = n // 2
        mask = 2 ** n2 - 1
        l1 = (k >> n2) & mask
        l2 = k & mask
        return l1, l2


    def mux(self, l, r, n):
        """
        # l, r - n-битовые числа
        # возвращает число (2n-битовое), являющееся конкатенацией бит этих чисел
        """
        y = 0
        y ^= r
        y ^= l << n
        return y


    def gf_multiply_modular(self, a, b, mod, n):
        """
        INPUTS
        a - полином (множимое)
        b - полином (множитель)
        mod - неприводимый полином
        n - порядок неприводимого полинома
        OUTPUTS:
        product - результат перемножения двух полиномов a и b
        """
        # маска для наиболее значимого бита в слове
        msb = 2 ** (n - 1)
        # маска на все биты
        mask = 2 ** n - 1
        # r(x) = x^n mod m(x)
        r = mod ^ (2 ** n)
        product = 0  # результат умножения
        mm = 1
        for i in range(n):
            if b & mm > 0:
                # если у множителя текущий бит 1
                product ^= a
            # выполняем последовательное умножение на х
            if a & msb == 0:
                # если старший бит 0, то просто сдвигаем на 1 бит
                a <<= 1
            else:
                # если старший бит 1, то сдвиг на 1 бит
                a <<= 1
                # и сложение по модулю 2 с r(x)
                a ^= r
                # берем только n бит
                a &= mask
            # формируем маску для получения очередного бита в множителе
            mm += mm
        return product


    def gf_divide(self, a, b):
        # деление полинома на полином
        # результат: частное, остаток (полиномы)
        dividend = a  # делимое
        divisor = b  # делитель
        a = 0
        # бит в делимом
        m = len(bin(dividend)) - 2
        # бит в делителе
        n = len(bin(divisor)) - 2
        s = divisor << m
        msb = 2 ** (m + n - 1)
        for i in range(m):
            dividend <<= 1
            if dividend & msb > 0:
                dividend ^= s
                dividend ^= 1
        maskq = 2 ** m - 1
        maskr = 2 ** n - 1
        r = (dividend >> m) & maskr
        q = dividend & maskq
        return q, r


    def gf_mi(self, b, m, n):
        """
        INPUTS
        b (integer)– полином, для которого надо найти обратное по умножению
        m (integer) – неприводимый полином
        n (integer)- порядок неприводимого полинома
        OUTPUTS:
        b2 (integer) – полином, обратный по умножению к b

        """


        a1, a2, a3 = 1, 0, m
        b1, b2, b3 = 0, 1, b

        while b3 != 1:
            q, r = self.gf_divide(a3, b3)
            b1, b2, b3, a1, a2, a3 = a1 ^ self.gf_multiply_modular(q, b1, m, n),\
                                     a2 ^ self.gf_multiply_modular(q, b2, m, n), \
                                     r, b1, b2, b3


        return b2


    def sbox(self, v):
        """
        Замена 4-битового значения по таблице S_Box
        """
        r, c = self.divide_into_two(v, 4)
        rez = self.S_Box[r, c]
        return int(rez, 16)

    def sbox_inv(self, v):
        """
        Замена 4-битового значения по таблице S_InvBox
        """
        r, c = self.divide_into_two(v, 4)
        rez = self.S_InvBox[r, c]
        return int(rez, 16)

    def g(self, w, i):
        """
        g функция в алгоритме расширения ключа
        """

        n00, n11 = self.divide_into_two(w, 8)
        n0 = self.sbox(n00)
        n1 = self.sbox(n11)
        n1n0 = self.mux(n1, n0, 4)
        if i == 1:
            rez = n1n0 ^ self.RCON1
        else:
            rez = n1n0 ^ self.RCON2
        return rez

    def key_expansion(self, key):
        """
        Алгоритм расширения ключа
        """
        w0, w1 = self.divide_into_two(key, 16)
        w2 = w0 ^ self.g(w1, 1)

        w3 = w1 ^ w2
        w4 = w2 ^ self.g(w3, 2)
        w5 = w3 ^ w4
        return key, self.mux(w2, w3, 8), self.mux(w4, w5, 8)

    def to_state_matrix(self, block):
        """
        Формирование матрицы состояния из 16-ти битового числа
        """

        b1, b2 = self.divide_into_two(block, 16)
        b11, b12 = self.divide_into_two(b1, 8)
        b21, b22 = self.divide_into_two(b2, 8)
        self.state_matrix = [[b11, b21], [b12, b22]]

    def add_round_key(self, k):
        """
        Сложение с раундовым ключом (Add round key)
        """

        k1, k2 = self.divide_into_two(k, 16)
        k11, k12 = self.divide_into_two(k1, 8)
        k21, k22 = self.divide_into_two(k2, 8)
        self.state_matrix[0][0] ^= k11
        self.state_matrix[1][0] ^= k12
        self.state_matrix[0][1] ^= k21
        self.state_matrix[1][1] ^= k22

    def nibble_substitution(self):
        """
        Замена элементов матрицы состояния S (Nibble Substitution)
        """

        self.state_matrix[0][0] = self.sbox(self.state_matrix[0][0])
        self.state_matrix[0][1] = self.sbox(self.state_matrix[0][1])
        self.state_matrix[1][0] = self.sbox(self.state_matrix[1][0])
        self.state_matrix[1][1] = self.sbox(self.state_matrix[1][1])

    def nibble_substitution_inv(self):
        """
        Обратная замена элементов матрицы состояния S (Inverse Nibble Substitution)
        """

        self.state_matrix[0][0] = self.sbox_inv(self.state_matrix[0][0])
        self.state_matrix[0][1] = self.sbox_inv(self.state_matrix[0][1])
        self.state_matrix[1][0] = self.sbox_inv(self.state_matrix[1][0])
        self.state_matrix[1][1] = self.sbox_inv(self.state_matrix[1][1])

    def shift_row(self):
        """
        Перестановка элементов в матрице состояния S (Shift Row)
        """

        a = self.state_matrix[1][0]
        self.state_matrix[1][0] = self.state_matrix[1][1]
        self.state_matrix[1][1] = a

    def mix_columns_(self, matrix):
        """
        Перемешивание прямое/обратное элементов в столбцах матрицы S (Mix Columns)
        """

        m00 = int(matrix[0][0], 16)
        m01 = int(matrix[0][1], 16)
        m10 = int(matrix[1][0], 16)
        m11 = int(matrix[1][1], 16)
        st00 = self.state_matrix[0][0]
        st10 = self.state_matrix[1][0]
        a = self.gf_multiply_modular(m00, st00, self.modulus, 4)
        b = self.gf_multiply_modular(m01, st10, self.modulus, 4)

        c = self.gf_multiply_modular(m10, st00, self.modulus, 4)
        d = self.gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][0] = a ^ b
        self.state_matrix[1][0] = c ^ d
        st00 = self.state_matrix[0][1]
        st10 = self.state_matrix[1][1]
        a = self.gf_multiply_modular(m00, st00, self.modulus, 4)
        b = self.gf_multiply_modular(m01, st10, self.modulus, 4)
        c = self.gf_multiply_modular(m10, st00, self.modulus, 4)
        d = self.gf_multiply_modular(m11, st10, self.modulus, 4)
        self.state_matrix[0][1] = a ^ b
        self.state_matrix[1][1] = c ^ d

    def mix_columns(self):
        """
        Перемешивание элементов в столбцах матрицы S (Mix Columns)
        """
        self.mix_columns_(self.column_Matrix)


    def mix_columns_inv(self):
        """
        Обратное перемешивание элементов в столбцах матрицы S (Inverse Mix Columns)
        """

        self.mix_columns_(self.column_InvMatrix)

    def from_state_matrix(self):
        """
        Формирование 16-ти битового числа из матрицы состояния
        """

        b1 = self.mux(self.state_matrix[0][0], self.state_matrix[1][0], 4)
        b2 = self.mux(self.state_matrix[0][1], self.state_matrix[1][1], 4)
        return self.mux(b1, b2, 8)

    def encrypt(self, plaintext, k0, k1, k2):
        """
        Алгоритм шифрования блока с заданными раундовыми ключами
        """
        self.to_state_matrix(plaintext)
        self.add_round_key(k0)

        # Первый раунд
        self.nibble_substitution()
        self.shift_row()
        self.mix_columns()
        self.add_round_key(k1)

        # Второй раунд
        self.nibble_substitution()
        self.shift_row()
        self.add_round_key(k2)

        return self.from_state_matrix()




    def decrypt(self, ciphertext, k0, k1, k2):
        """
        Алгоритм расшифрования блока с заданными раундовыми ключами
        """
        self.to_state_matrix(ciphertext)
        self.add_round_key(k2)

        # Первый раунд
        self.shift_row()
        self.nibble_substitution_inv()
        self.add_round_key(k1)
        self.mix_columns_inv()

        # Второй раунд
        self.shift_row()
        self.nibble_substitution_inv()
        self.add_round_key(k0)

        return self.from_state_matrix()




    def encrypt_data(self, data, key):
        """
        шифрование 16-битовых чисел в data на ключе key
        """

        k0, k1, k2 = self.key_expansion(key)
        cypher_data = []
        for x in data:
            c = self.encrypt(x, k0, k1, k2)
            cypher_data.append(c)
        return cypher_data

    def decrypt_data(self, data, key):
        """
        шифрование 16-битовых чисел в data на ключе key
        """

        k0, k1, k2 = self.key_expansion(key)
        dec_data = []
        for x in data:
            d = self.decrypt(x, k0, k1, k2)
            dec_data.append(d)
        return dec_data

    def cbcEncrypt(self, data, key, iv):
        k0, k1, k2 = self.key_expansion(key)

        cypher_data = []
        prev = iv
        for m in data:
            c = m ^ prev
            c = self.encrypt(c, k0, k1, k2)
            cypher_data.append(c)
            prev = c
        return cypher_data

    def сbcDecrypt(self, cypher_data, key, iv):
        k0, k1, k2 = self.key_expansion(key)
        data = []
        prev = iv
        for c in cypher_data:
            m = self.decrypt(c, k0, k1, k2)
            m ^= prev
            data.append(m)
            prev = c
        return data

    def ofbCrypt(self, data, key, iv):
        k0, k1, k2 = self.key_expansion(key)
        cypher_data = []
        s = iv
        for m in data:
            s = self.encrypt(s, k0, k1, k2)
            c = m ^ s
            cypher_data.append(c)
        return cypher_data

    def cfbEncrypt(self, data, key, iv, segment_size):
        k0, k1, k2 = self.key_expansion(key)
        cypher_data = []
        sreg = iv
        for m in data:
            e = self.encrypt(sreg, k0, k1, k2)
            e = e >> (16 - segment_size)
            c = m ^ e
            cypher_data.append(c)
            sreg = ((sreg << segment_size) | c) & 0xffff

        return cypher_data

    def сfbDecrypt(self, cypher_data, key, iv, segment_size):
        k0, k1, k2 = self.key_expansion(key)
        data = []
        sreg = iv
        for c in cypher_data:
            m = self.encrypt(sreg, k0, k1, k2)
            m = m >> (16 - segment_size)
            p = m ^ c
            data.append(p)
            sreg = ((sreg << segment_size) | c) & 0xffff
        return data

    def ctrCrypt(self, data, key, iv):
        k0, k1, k2 = self.key_expansion(key)
        out = []
        counter = iv
        for m in data:
            e = self.encrypt(counter, k0, k1, k2)
            c = m ^ e
            out.append(c)
            counter = (counter + 1) & 0xffff
        return out


    def Encrypt_mod(self, data, key, mode, iv=None, segment_size=16):
        if mode == 'CBC':
            return self.cbcEncrypt(data, key, iv)
        elif mode == 'OFB':
            return self.ofbCrypt(data, key, iv)
        elif mode == 'CFB':
            return self.cfbEncrypt(data, key, iv, segment_size)
        elif mode == 'CTR':
            return self.ctrCrypt(data, key, iv)

    def Decrypt_mod(self, data, key, mode, iv=None, segment_size=16):
        if mode == 'CBC':
            return self.сbcDecrypt(data, key, iv)
        elif mode == 'OFB':
            return self.ofbCrypt(data, key, iv)
        elif mode == 'CFB':
            return self.сfbDecrypt(data, key, iv, segment_size)
        elif mode == 'CTR':
            return self.ctrCrypt(data, key, iv)
