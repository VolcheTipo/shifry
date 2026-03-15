from hill_utils import hill_decrypt, recover_key


def task3_4(input_file, output_file, task_name):
    # Стандартный заголовок PNG (первые 4 байта)
    # 137, 80, 78, 71 (в десятичной системе)
    known_plain = bytes([137, 80, 78, 71]) #89, 50, 4e, 47

    try:
        with open(input_file, 'rb') as f:
            data = f.read()
        known_cipher = data[:4]
        print(f"{task_name}: Восстановление ключа...")
        key = recover_key(known_plain, known_cipher)
        if key:
            print(f"{task_name}: Ключ найден: {key}")
            decrypted_data = hill_decrypt(data, key)

            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            print(f"{task_name}: Файл сохранен как {output_file}")
        else:
            print(f"{task_name}: Не удалось восстановить ключ (определитель матрицы открытого текста не обратим).")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")


if __name__ == "__main__":
    # Задание 3
    task3_4('p1_hill_c_all.png', 'p1_hill_decrypted.png', "Задание 3")

    # Задание 4
    task3_4('b4_hill_c_all.png', 'b4_hill_decrypted.png', "Задание 4")