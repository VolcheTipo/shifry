import spn1

def task5():
    #decrypt() для одного блока
    e = spn1.SPN1()
    x = 9911
    k = 982832703
    rk = e.round_keys(k)
    y = e.encrypt(x, rk, rounds=4)
    lk = e.round_keys_to_decrypt(k)
    x_ = e.decrypt(y, lk, rounds=4)
    print(f'x = {bin(x)[2:].zfill(16)}')
    print(f'y = {bin(y)[2:].zfill(16)}')
    print(f'x_ = {bin(x_)[2:].zfill(16)}')
    print(f'Расшифрование верно: {x == x_}\n')

if __name__ == "__main__":
    task5()