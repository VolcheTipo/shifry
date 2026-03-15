import Caesar, afin_shifr
import read_write_file
import detectEnglish
import random



def main():
    ###ЧАСТЬ 1###
    #1-9
    m = 24
    key = 37
    c = Caesar.encrypt(m, key)
    print('c=', c)
    m1 = Caesar.decrypt(c, key)
    print('m1=', m1)
    data = [34, 67, 123, 79, 201]
    encrypt_data = Caesar.encrypt_data(data, key)
    print('encrypt_data=', encrypt_data)
    decrypt_data = Caesar.decrypt_data(encrypt_data, key)
    print('decrypt_data=', decrypt_data, '\n')

    #10-12
    data = read_write_file.read_data_1byte('f1.txt')
    print('data=', data[0:15])
    txt = ''
    for n in data[0:15]:
        txt += chr(n)
    print('text=', txt, '\n')

    #13
    data = read_write_file.read_data_1byte('f1.txt')
    print('data=', data[0:15])
    encrypt_data = Caesar.encrypt_data(data, key=67)
    print('encrypt_data=', encrypt_data[0:15])
    txt = ''.join([chr(n) for n in encrypt_data[0:15]])
    print('encrypt_text=', txt)
    read_write_file.write_data_1byte('f1_encrypt.txt', encrypt_data) #f1_encrypt создаем пустым
    print('\n')
    #14
    encrypt_data = read_write_file.read_data_1byte('f1_encrypt.txt')
    print('encrypt_data=', encrypt_data[0:15])
    decrypt_data = Caesar.decrypt_data(encrypt_data, key=67)
    print('decrypt_data=', decrypt_data[0:15])
    txt = ''.join([chr(n) for n in decrypt_data[0:15]])
    print('decrypt_data=', txt)
    read_write_file.write_data_1byte('f1_decrypt.txt', decrypt_data)
    print('\n')
    #15
    decrypt_data = Caesar.decrypt_data(decrypt_data, key)
    txt = ''.join([chr(n) for n in decrypt_data])
    print('decrypt_data=', txt)
    is_english = detectEnglish.isEnglish(txt)
    print('is_english=', is_english, '\n')

    ###ЧАСТЬ 2###
    #1
    data = read_write_file.read_data_1byte('f2.png')
    encrypt_data = Caesar.encrypt_data(data, key=143)
    read_write_file.write_data_1byte('f2_encrypt.png', encrypt_data)
    decrypt_data = Caesar.decrypt_data(encrypt_data, key=143)
    read_write_file.write_data_1byte('f2_decrypt.png', decrypt_data)

    #1.2
    # 89 в 16-ной = 137 в 10-ной; 50 в 16-ной = 80 в 10-ной

    with open('f2_encrypt.png', 'rb') as f:
        encrypted = f.read()
    # Ищем ключ
    found_key = None
    for key in range(256):
        if (encrypted[0] - key) % 256 == 137 and (encrypted[1] - key) % 256 == 80:
            found_key = key
            break

    if found_key is not None:
        print(f"Найден ключ: {found_key}", "\n")
        decrypted= Caesar.decrypt_data(encrypted, key=found_key)
        read_write_file.write_data_1byte('f2_decrypt1.png', decrypt_data)
    else:
        print("Ключ не найден\n")

    #2 - задание для нечёт варианта (13 номер в группе)
    #
    #с использованием isEnglish из части 1 про текстовые шифры
    encrypted_data = read_write_file.read_data_1byte('t3_caesar_c_all.txt')
    for key in range(256):
        decrypt_data = Caesar.decrypt_data(encrypted_data, key)
        txt = ''.join([chr(n) for n in decrypt_data])
        is_english = detectEnglish.isEnglish(txt)
        if is_english:
            with open(f'decrypted_key_{key}.txt', 'w', encoding='utf-8') as f:
                f.write(txt)
            break
    else:
        print('Правильный ключ не найден\n')

    #4
    # Таблица замен
    k = [179, 109, 157, 182, 126, 141, 251, 220, 169, 237, 188, 131, 207, 22, 32, 242,
         208, 68, 216, 170, 249, 199, 44, 198, 206, 8, 148, 197, 136, 195, 159, 98, 175,
         53, 123, 212, 233, 150, 6, 243, 38, 79, 156, 153, 2, 134, 47, 215, 102, 15, 57,
         110, 236, 24, 184, 72, 137, 113, 171, 70, 161, 64, 252, 247, 49, 103, 105, 138,
         119, 213, 87, 130, 203, 90, 167, 238, 231, 116, 78, 86, 173, 250, 200, 239, 178,
         97, 114, 94, 166, 142, 104, 31, 75, 89, 106, 56, 128, 69, 164, 67, 26, 228, 61,
         181, 125, 227, 54, 96, 168, 107, 17, 14, 37, 190, 219, 211, 121, 112, 35, 18, 143,
         158, 193, 129, 71, 23, 101, 191, 41, 241, 82, 201, 223, 120, 59, 177, 58, 63, 151,
         42, 36, 183, 226, 127, 172, 202, 84, 132, 3, 45, 73, 30, 235, 50, 189, 4, 1, 43,
         221, 205, 83, 232, 46, 147, 93, 192, 124, 244, 12, 21, 80, 55, 160, 145, 245, 209,
         88, 204, 176, 13, 253, 11, 99, 165, 140, 19, 224, 111, 27, 185, 65, 62, 16, 163,
         210, 115, 217, 34, 92, 187, 152, 155, 108, 5, 122, 229, 174, 118, 162, 95, 100, 7,
         66, 29, 230, 144, 149, 52, 9, 91, 117, 214, 76, 48, 33, 194, 254, 10, 234, 218, 40,
         133, 196, 139, 135, 240, 60, 25, 225, 85, 255, 246, 51, 28, 146, 74, 222, 186, 39,
         77, 0, 20, 180, 154, 81, 248]

    # Обратная таблица замен inv_k
    inv_k = [0] * 256
    for m, c in enumerate(k):
        inv_k[c] = m
    with open('c3_subst_c_all.png', 'rb') as f:
        encrypted_data = f.read()
    # Расшифровываем каждый байт с помощью inv_k
    decrypted_data = bytes(inv_k[c] for c in encrypted_data)
    print(f"Первые два байта расшифрованного файла: {decrypted_data[:2].hex()}")
    if decrypted_data[:2] == b'\x89\x50':
        print("Сигнатура PNG верна!")
    else:
        print("Ошибка: сигнатура PNG неверна.")
    with open('decrypted4.png', 'wb') as f:
        f.write(decrypted_data)
    print("Файл успешно расшифрован и сохранен как 'decrypted4.png'\n")

    #5
    #Афинный шифр

    #6
    


if __name__ == '__main__':
    main()