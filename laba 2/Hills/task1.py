from hill_utils import hill_decrypt


def task1():
    input_file = 'im3_hill_c_all.bmp'
    output_file = 'im3_hill_decrypted.bmp'
    key = [[189, 58], [21, 151]]
    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        decrypted_data = hill_decrypt(data, key)

        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        print(f"Задание выполнено. Файл сохранен как {output_file}")
    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка при расшифровке: {e}")


if __name__ == "__main__":
    task1()