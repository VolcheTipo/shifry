###############
# SPN1
###############

class SPN1():
    #p-box (прямая перестановка битов 16-битного слова)
    p = [0, 4, 8, 12, 1, 5,
         9, 13, 2, 6, 10, 14,
         3, 7, 11, 15]
    #S-box (замена 4-битного числа)
    s = [14, 4, 13, 1, 2, 15, 11, 8,
         3, 10, 6, 12, 5, 9, 0, 7]

    #для третьего номера
    # часть а — обратная замена (asbox) уже определена выше
    # часть б — обратная перестановка (apbox) уже определена выше
    # часть в — проверка свойств выполняется в task3.py

    def __init__(self):
        # Обратный S-box: inv_s_box[значение] = исходный индекс
        self.inv_s_box = [0] * 16
        for i, val in enumerate(self.s):
            self.inv_s_box[val] = i

        # Обратная P-box: inv_p_box[новая_позиция] = исходная_позиция
        self.inv_p_box = [0] * 16
        for old_pos, new_pos in enumerate(self.p):
            self.inv_p_box[new_pos] = old_pos

    # s-box (прямая замена для одного 4-битного числа)
    def sbox(self, x):
        return self.s[x]

    # p-box (прямая перестановка для 16-битного числа)
    def pbox(self, x):
        y = 0
        for i in range(len(self.p)):
            if (x & (1 << i)) != 0:
                y ^= (1 << self.p[i])
        return y

    # обратная s-box для одного 4-битного числа
    def asbox(self, x):
        return self.inv_s_box[x]

    # обратная p-box для 16-битного числа
    def apbox(self, x):
        y = 0
        for i in range(16):          # i – новая позиция бита
            if (x & (1 << i)) != 0:
                y |= (1 << self.inv_p_box[i])
        return y

    # demux
    def demux(self, x):
        # x целое число от 0 до 65535 (16 бит)
        y = []
        for i in range(0, 4):
            # x >> (i*4) сдвигает биты числа вправо на i*4 позиций,
            # чтобы нужный 4-битный блок оказался в младших разрядах
            y.append((x >> (i*4)) & 0xf)  # =1111. зануляет все биты старше 4-х,
                                           # оставляя только младшие 4 бита
        return y
    # порядок битов: y[3]y[2]y[1]y[0]

    # mux
    def mux(self, x):
        # х список из четырёх целых чисел (каждое от 0 до 15)
        y = 0
        for i in range(0, 4):
            y ^= (x[i] << (i*4))  # XOR. Добавляет этот сдвинутый блок к итоговому числу
                                   # (в скобках: сдвигает значение i-го блока влево на
                                   # соответствующее количество битов, чтобы он занял
                                   # правильную позицию в 16-битном слове)
        return y

    def round_keys(self, k):
        rk = []
        rk.append((k >> 16) & (2**16-1))
        rk.append((k >> 12) & (2**16-1))
        rk.append((k >> 8) & (2**16-1))
        rk.append((k >> 4) & (2**16-1))
        rk.append(k & (2**16-1))
        return rk

    # Key mixing
    def mix(self, p, k):
        v = p ^ k
        return v

    # round function
    def round(self, p, k):
        # XOR key
        u = self.mix(p, k)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        # run through permutation layer
        w = self.pbox(self.mux(v))
        return w

    def last_round(self, p, k1, k2):
        # XOR key
        u = self.mix(p, k1)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        # XOR key
        u = self.mix(self.mux(v), k2)
        return u

    def encrypt(self, p, rk, rounds):
        x = p
        for i in range(rounds-1):
            x = self.round(x, rk[i])
        x = self.last_round(x, rk[rounds-1], rk[rounds])
        return x

    ###################### добавленная, №2 ########################
    def encrypt_data(self, data, key, rounds=4):
        # Шифрование списка 16-битных чисел
        rk = self.round_keys(key)
        result = []
        for x in data:
            result.append(self.encrypt(x, rk, rounds))
        return result

    ###################### добавленная, №4 #########################
    # Генерация ключей для расшифрования
    def round_keys_to_decrypt(self, key):
        rk = self.round_keys(key)
        # Для расшифрования ключи используются в обратном порядке,
        # но ко всем, кроме первого и последнего, применяется обратная перестановка
        L = [rk[4], rk[3], rk[2], rk[1], rk[0]]
        for i in [1, 2, 3]:
            L[i] = self.apbox(L[i])
        return L

    ###################### добавленная, №5 ############################
    def decrypt(self, y, lk, rounds=4):
        # Расшифровка одного 16-битного блока с использованием ключей lk,
        # полученных от round_keys_to_decrypt.
        # Восстанавливаем исходные ключи шифрования из lk:
        K4 = lk[0]
        K3 = self.pbox(lk[1])
        K2 = self.pbox(lk[2])
        K1 = self.pbox(lk[3])
        K0 = lk[4]
        state = y
        # Обратный последнему раунду (round 3)
        state = state ^ K4
        nibbles = self.demux(state)
        nibbles = [self.asbox(n) for n in nibbles]
        state = self.mux(nibbles) ^ K3
        # Обратный раунд 2
        state = self.apbox(state)
        nibbles = self.demux(state)
        nibbles = [self.asbox(n) for n in nibbles]
        state = self.mux(nibbles) ^ K2
        # Обратный раунд 1
        state = self.apbox(state)
        nibbles = self.demux(state)
        nibbles = [self.asbox(n) for n in nibbles]
        state = self.mux(nibbles) ^ K1
        # Обратный раунд 0
        state = self.apbox(state)
        nibbles = self.demux(state)
        nibbles = [self.asbox(n) for n in nibbles]
        state = self.mux(nibbles) ^ K0

        return state
    ############### добавленная, №6##############
    def decrypt_data(self, data, key, rounds=4):
        # Расшифрование списка 16-битных чисел
        lk = self.round_keys_to_decrypt(key)
        result = []
        for x in data:
            result.append(self.decrypt(x, lk, rounds))
        return result


def main():
    e = SPN1()
    x = int('1010010100010111', 2)
    rounds = 4
    k = int('01101100011101010100111100100001', 2)
    rk = e.round_keys(k)
    y = e.encrypt(x, rk, rounds)
    print('y={}'.format(bin(y)[2:].zfill(16)))


if __name__ == '__main__':
    main()