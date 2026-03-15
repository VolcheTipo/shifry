def vigenere_cipher(data, key, mode='decrypt', skip_bytes=0):
    key = [ord(c) for c in key]  # Преобразуем ключ в числовые значения
    result = bytearray()

    for i, byte in enumerate(data):
        if i < skip_bytes and mode == 'encrypt':
            result.append(byte)
        else:
            key_index = (i - (skip_bytes if mode == 'encrypt' else 0)) % len(key)
            if mode == 'encrypt':
                # Шифрование: (байт + ключ) mod 256
                new_byte = (byte + key[key_index]) % 256
            else:  # 'decrypt'
                # Дешифрование: (байт - ключ) mod 256
                new_byte = (byte - key[key_index]) % 256
            result.append(new_byte)

    return bytes(result)


def compare_files(file1, file2):
    #Сравнивает два файла побайтово.
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    if len(data1) != len(data2):
        print("Файлы разной длины!")
        return False

    errors = 0
    for i in range(len(data1)):
        if data1[i] != data2[i]:
            errors += 1
            if errors <= 10:  #первые 10 различий
                print(f"Различие в байте {i}: {data1[i]} != {data2[i]}")

    if errors == 0:
        print("Файлы идентичны!")
        return True
    else:
        print(f"Найдено {errors} различий")
        return False


def main():
    key = 'magistr'
    input_file = 'im6_vigener_c_all.bmp'
    decrypted_file = 'im6_decrypted.bmp'
    re_encrypted_file = 'im6_re_encrypted.bmp'

    # 1. Читаем зашифрованный файл
    print("Чтение зашифрованного файла...")
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    # 2. Расшифровываем файл
    print("Расшифровка файла ...")
    decrypted_data = vigenere_cipher(encrypted_data, key, 'decrypt', skip_bytes=0)

    # 3. Сохраняем расшифрованный файл
    print("Сохранение расшифрованного файла...")
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_data)

    # 4. Зашифровываем расшифрованный файл снова, пропуская первые 50 байт
    print("Повторное шифрование файла (первые 50 байт без изменений)...")
    re_encrypted_data = vigenere_cipher(decrypted_data, key, 'encrypt', skip_bytes=50)

    # 5. Сохраняем повторно зашифрованный файл
    print("Сохранение повторно зашифрованного файла...")
    with open(re_encrypted_file, 'wb') as f:
        f.write(re_encrypted_data)
    # 6. Сравниваем с оригиналом
    print("\nСравнение с оригинальным зашифрованным файлом:")
    compare_files(input_file, re_encrypted_file)


if __name__ == "__main__":
    main()