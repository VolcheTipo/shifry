class SDes():
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    LS1 = [2, 3, 4, 5, 1]
    LS2 = [3, 4, 5, 1, 2]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IPinv = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    SW = [5, 6, 7, 8, 1, 2, 3, 4]

    # таблицы замен
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]

    def __init__(self):
        #раундовые ключи. рассчитываются в функции key_schedule
        self.k1 = 0
        self.k2 = 0

    @staticmethod
    def pbox(x, p, nx):
        # перестановка бит в nx-битовом числе x по таблице перестановок p
        y = 0
        np = len(p)
        for i in reversed(range(np)):
            if (x & (1 << (nx - 0 - p[i]))) != 0:
                y ^= (1 << (np - 1 - i))
        return y
    def p10(self, x):
        return self.pbox(x, self.P10, 10)
    def p8(self, x):
        return self.pbox(x, self.P8, 10)
    def p4(self, x):
        return self.pbox(x, self.P4, 4)
    def ip(self, x):
        return self.pbox(x, self.IP, 8)
    def ipinv(self, x):
        return self.pbox(x, self.IPinv, 8)
    def ep(self, x):
        return self.pbox(x, self.EP, 4)
    def sw(self, x):
        return self.pbox(x, self.SW, 8)
    def ls1(self, x):
        return self.pbox(x, self.LS1, 5)
    def ls2(self, x):
        return self.pbox(x, self.LS2, 5)

    @staticmethod
    def divide_into_two(k, n):
        #функция разделяет n-битовое число k на два (n/2)-битовых числа
        n2 = n // 2
        mask = 2 ** n2 - 1
        l1 = (k >> n2) & mask
        l2 = k & mask
        return l1, l2

    @staticmethod
    def mux(l, r, n):
        #l, r - n-битовые числа
        #возвращает число (2n-битовое), являющееся конкатенацией бит этих чисел
        y = 0
        y ^= r
        y ^= l << n
        return y

    @staticmethod
    def apply_subst(x, s):
        #замена по таблице s
        r = 2 * (x >> 3) + (x & 1)
        c = 2 * ((x >> 2) & 1) + ((x >> 1) & 1)
        return s[r][c]

    def s0(self, x):
        #замена по таблице s0
        return self.apply_subst(x, self.S0)

    def s1(self, x):
        #замена по таблице s1
        return self.apply_subst(x, self.S1)