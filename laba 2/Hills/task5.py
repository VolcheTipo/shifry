from hill_utils import hill_decrypt, recover_key

def solve_task5():
    input_file = 'text2_hill_c_all.txt'
    output_file = 'text2_hill_decrypted.txt'
    # Известное начало текста
    known_text_str = "Whos"  # 4 байта достаточно для матрицы 2x2
    known_plain = known_text_str.encode('ascii')

    try:
        with open(input_file, 'rb') as f:
            data = f.read()
        known_cipher = data[:4]
        print("Восстановление ключа по тексту 'Whos'...")
        key = recover_key(known_plain, known_cipher)
        if key:
            print(f"Ключ найден: {key}")
            decrypted_data = hill_decrypt(data, key)
            # Пробуем декодировать в строку для проверки, но сохраняем как байты
            try:
                print("Первые 100 символов расшифрованного текста:")
                print(decrypted_data[:100].decode('ascii', errors='ignore'))
            except:
                pass

            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            print(f"Файл сохранен как {output_file}")
        else:
            print("Не удалось восстановить ключ.")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    solve_task5()