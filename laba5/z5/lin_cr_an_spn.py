__author__ = 'рс'


import random
from spn1 import SPN1

###############
# linear analysis of SPN1
###############


# возвращает значение бита на позиции pos в числе x
def grab(x, pos):
    return (x >> pos) & 1


def find_bias(spn):

    #2-d list to store bias, indexed by masks.
    # Format is bias[input][output]
    bias = []
    T = []
    vals = len(spn.s)

    for xi in range(vals):
        for yi in range(vals):
            count = 0
            for k_in in range(vals):
                k_out = spn.sbox(k_in)
                xk = xi&k_in
                yk = yi&k_out
                orxk = grab(xk, 0) ^ grab(xk, 1) ^ grab(xk, 2) ^ \
                        grab(xk, 3)
                oryk = grab(yk, 0) ^ grab(yk, 1) ^ grab(yk, 2) ^ \
                        grab(yk, 3)

                if orxk ^ oryk == 0:
                    count += 1
            T.append(count-vals/2)
        bias.append(T)
        print(T)
        T = []
    return bias


#find the input/output masks with bias x
def find_masks(b, x):
    r = []
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] == x:
                r.append("{0},{1}".format(i,j))

    return r

#find the key
def attack0(e, k, rounds):
    # формируем достаточное количество пар plaintaext-ciphertext
    plaintext = []
    ciphertext = []
    numpairs = 1*8000
    rk = e.round_keys(k)
    for i in range(numpairs):
        p = random.randint(0, 2**16)
        plaintext.append(p)
        c = e.encrypt(p, rk, rounds)
        ciphertext.append(c)
    #holds best deviation so far
    maxdev = -1
    #holds best k so far
    maxk = -1
    # ищем 8 бит подключа K5, всего 256 вариантов
    ssize = 256
    # обнуляем массив счетчиков
    count = [0 for i in range(ssize)]
    # цикл по количеству подключей
    for k1 in range(ssize):
        # для каждой пары plaintext-ciphertext
        for j in range(0, len(plaintext)):
            x = plaintext[j]
            y = ciphertext[j]
            # формируем подключ в виде (l1,l2)
            l1 = (k1 >> 4) & 15
            l2 = k1 & 15
            # выделяем в ciphertext соответствующие (l1,l2) участки
            y_2 = (y >> 8) & 15
            y_4 = y & 15
            # XOR
            v_2 = y_2 ^ l1
            v_4 = y_4 ^ l2
            # inverse sbox
            u_2 = e.asbox(v_2)
            u_4 = e.asbox(v_4)
            # If the linear expression holds, increment
            # the appropriate count
            if grab(x, 8) ^ grab(x, 9) ^ grab(x, 11) ^ \
                grab(u_2, 0) ^ grab(u_2, 2) ^ grab(u_4, 0) ^ \
                    grab(u_4, 2) == 0:
                            count[k1] += 1
        print('k={}'.format(k1))
        print('count[{}]={} bias:{}'.format(k1, count[k1], numpairs/2-count[k1]))
        # If this was the best so far, then mark it
        if abs(count[k1] - len(plaintext)/2) >= maxdev:
            maxdev = abs(count[k1] - len(plaintext)/2)
            maxk = k1
    print(maxk, maxdev)
    print("RESULT: {0}, deviation: {1}, bias: {2}".format(maxk, maxdev, float(maxdev)/numpairs))
    l1 = (maxk >> 4) & 15
    l2 = maxk & 15
    print("(L1, L2)=({}, {}) = ({}, {}))".format(l1, l2, SPN1.binary(l1, 4), SPN1.binary(l2, 4)))
    rk = e.round_keys(k)
    print('k5={}'.format(SPN1.binary(rk[4], 16)))

def prim0():
    # решение из описания
    s = [15, 7, 10, 2, 13, 12, 0, 6, 3, 14, 9, 1, 11, 4, 5, 8]
    p = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    e = SPN1(s, p)
    rounds = 4
    k = int('00111010100101001101011000111110', 2)

    print('k={}'.format(k))
    rk = e.round_keys(k)
    bias = find_bias(e)
    print("highest biases:")
    print("6: {0}".format(find_masks(bias, 6)))
    print("4: {0}".format(find_masks(bias, 4)))
    # print("2: {0}".format(findMasks(bias, 2)))
    print("-6: {0}".format(find_masks(bias, -6)))
    print("-4: {0}".format(find_masks(bias, -4)))
    print("-2: {0}".format(find_masks(bias, -2)))
    attack0(e, k, rounds)
    e.print_s_p()
    print('----------------------')

def main():
    prim0()   # пример из описания лин. кр-а в задании (8 бит)

if __name__ == '__main__':
    main()