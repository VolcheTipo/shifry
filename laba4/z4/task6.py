import spn1

def task6():
    #decrypt_data()
    e = spn1.SPN1()
    x = [9911, 12432, 456, 21]
    k = 982832703
    y = e.encrypt_data(x, k, rounds=4)
    x_ = e.decrypt_data(y, k, rounds=4)
    print(f'x = {x}')
    print(f'y = {y}')
    print(f'x_ = {x_}')
    print(f'Расшифрование верно: {x == x_}\n')


if __name__ == "__main__":
    task6()