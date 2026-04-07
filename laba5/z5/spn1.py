
###############
# SPN1
###############


class SPN1():

    def __init__(self, s, p):
        """
        s - таблица замен (список из 16 элементов)
        p - таблица перестановок (список из 16 элементов)
        """
        self.s = s
        self.p = p
        # обратная таблица замен
        self.s_inv = [0] * 16
        for i in range(16):
            self.s_inv[s[i]] = i

    # s-box
    def sbox(self, x):
        return self.s[x]

    # p-box
    def pbox(self, x):
        y = 0
        for i in range(len(self.p)):
            if (x & (1 << i)) != 0:
                y ^= (1 << self.p[i])
        return y

    def asbox(self, x):
        #Обратная замена S-блока
        return self.s_inv[x]

    # break into 4-bit chunks
    def demux(self, x):
        y = []
        for i in range(0, 4):
            y.append((x >> (i*4)) & 0xf)
        return y


    #convert back into 16-bit state
    def mux(self, x):
        y = 0
        for i in range(0, 4):
            y ^= (x[i] << (i*4))
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

    #round function
    def round(self, p, k):
        #XOR key
        u = self.mix(p, k)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        # run through permutation layer
        w = self.pbox(self.mux(v))
        return w

    def last_round(self, p, k1, k2):
        #XOR key
        u = self.mix(p, k1)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        #XOR key
        u = self.mix(self.mux(v), k2)
        return u

    def encrypt(self, p, rk, rounds):
        x = p
        for i in range(rounds-1):
            x = self.round(x, rk[i])
        x = self.last_round(x, rk[rounds-1], rk[rounds])
        return x

    def binary(x, n):
        """Преобразует число x в двоичную строку длиной n бит"""
        return format(x, '0{}b'.format(n))

    def print_s_p(self):
        """Вывод таблиц"""
        print("S-box:", self.s)
        print("P-box:", self.p)


