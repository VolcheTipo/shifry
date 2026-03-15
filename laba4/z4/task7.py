from read_write_file import read_data_2byte as read2
from read_write_file import write_data_2byte as write2
import spn1


def task7():
    e = spn1.SPN1()
    key = 452342216
    rounds = 4

    # Чтение исходного файла
    print("Чтение исходного файла")
    data_original = read2('123.txt')
    print(f"Исходные данные: {data_original[:20]}")
    print(f"Длина исходных данных: {len(data_original)}", "\n")
    # Шифрование
    print("Шифрование")
    cipher_data = e.encrypt_data(data_original, key, rounds)
    print(f"Зашифрованные данные: {cipher_data[:20]}")
    # Проверка: зашифрованный файл должен отличаться
    if data_original != cipher_data:
        print("Зашифрованные данные ОТЛИЧАЮТСЯ от исходных\n")
    else:
        print("Зашифрованные данные СОВПАДАЮТ с исходными!\n")

    write2('123_encrypt.txt', cipher_data)

    # Чтение зашифрованного файла
    print("Чтение зашифрованного файла")
    data_enc = read2('123_encrypt.txt')
    print(f"Прочитанные зашифрованные данные: {data_enc[:20]}")

    # Проверка совпадения записанных и прочитанных зашифрованных данных
    if cipher_data == data_enc:
        print("Запись/чтение зашифрованного файла работает корректно\n")
    else:
        print("Проблема с записью/чтением зашифрованного файла!\n")
    # Расшифрование
    print("Расшифрование")
    decrypt_data = e.decrypt_data(data_enc, key, rounds)
    print(f"Расшифрованные данные: {decrypt_data[:20]}", "\n")
    write2('123_decrypt.txt', decrypt_data)
    # Финальная проверка
    print("ФИНАЛЬНАЯ ПРОВЕРКА")
    if data_original == decrypt_data:
        print("УСПЕХ. Расшифрованный файл СОВПАДАЕТ с исходным")
        print("Задание выполнено правильно")
    else:
        print("ОШИБКА. Расшифрованный файл НЕ совпадает с исходным")
        print(f"Длина исходного: {len(data_original)}, расшифрованного: {len(decrypt_data)}")
        # Найдем первое различие
        for i in range(min(len(data_original), len(decrypt_data))):
            if data_original[i] != decrypt_data[i]:
                print(f"Первое различие на позиции {i}: {data_original[i]} vs {decrypt_data[i]}")
                break


if __name__ == '__main__':
    task7()