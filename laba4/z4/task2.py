import spn1

def task2():
    e = spn1.SPN1()
    data = [15324, 3453, 34, 12533]
    k = 734533245
    cipher_data = e.encrypt_data(data, key=k, rounds=4)
    print(f'data = {data}')
    print(f'cipher_data = {cipher_data}\n') #данные верны(сверены с заданием)


if __name__ == "__main__":
    task2()