import spn1
#блоками называем в нашей лабе связку из 4х битиков

def task1():
    e = spn1.SPN1()
    # Демонстрация demux
    x = 15324
    print('x={}'.format(bin(x)[2:].zfill(16)))
    y = e.demux(x)
    print('y={}'.format(y))
    print("demux() разбивает 16-битное число на 4 блока (по 4 бита)\n")
    #перевод из двоичной в 16ричку по 4 блока + инверсия

    # Демонстрация mux
    x_list = [9, 11, 4, 2]
    print(x_list)
    y = e.mux(x_list)
    print('y={}'.format(bin(y)[2:].zfill(16)))
    print("mux() собирает 4 блока в 16-битное число\n")
    #перевод из 16рички в двоичку + инверсия

if __name__ == "__main__":
    task1()