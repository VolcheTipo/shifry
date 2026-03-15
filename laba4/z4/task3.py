import spn1
def task3():
    #asbox, apbox, проверка свойств
    #asbox =  обратная замена (добавляем в spn1)
    #apbox = перестановка (добавляем в spn1)
    #проверка свойств: pi^(-1)_p (x xor y) = pi^(-1)_p (x) xor pi^(-1)_p (y)
    e = spn1.SPN1()

    #часть а
    #прямая + обратная замена
    x = 9
    sx = e.sbox(x)
    x_ = e.asbox(sx)
    print(f'asbox(sbox({x})) = {x_} (должно быть {x})')

    #часть б
    p = [2, 5, 6, 8, 4, 14, 0, 7, 11, 10, 12, 1, 15, 9, 3, 13]
    x = int('0010011010110111', 2)
    px = e.pbox(x)
    x_ = e.apbox(px)
    print(f'apbox(pbox(x)) = {bin(x_)[2:].zfill(16)} (должно быть {bin(x)[2:].zfill(16)})')

    #часть в
    x = 15324
    y = 24681
    px = e.pbox(x)
    py = e.pbox(y)
    p_xor = e.pbox(x ^ y)
    xor_p = px ^ py
    print(f'πP(x⊕y) = {p_xor}, πP(x)⊕πP(y) = {xor_p}')
    print(f'Свойство выполнено: {p_xor == xor_p}\n')


if __name__ == "__main__":
    task3()