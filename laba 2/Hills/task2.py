from hill_utils import hill_decrypt, hill_encrypt


def task2():
    input_file = 'm18_hill_c_all.bmp'
    decrypted_file = 'm18_hill_decrypted.bmp'
    reencrypted_file = 'm18_hill_reencrypted.bmp'

    key = [[47, 239], [119, 108]]

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        decrypted_data = hill_decrypt(data, key)
        with open(decrypted_file, 'wb') as f:
            f.write(decrypted_data)
        print(f"Шаг 1: Расшифровка выполнена. Сохранено в {decrypted_file}")

        # 2. Шифрование с пропуском первых 50 байт
        # Применяем шифрование к расшифрованным данным, но байты 0-49 не трогаем
        reencrypted_data = hill_encrypt(decrypted_data, key, skip_bytes=50)

        with open(reencrypted_file, 'wb') as f:
            f.write(reencrypted_data)
        print(f"Шаг 2: Повторное шифрование (с пропуском 50 байт) выполнено. Сохранено в {reencrypted_file}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    task2()