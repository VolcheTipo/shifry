from read_write_file import read_data_1byte
import detectEnglish

KNOWN_TEXT = "it therefore"
KNOWN_BYTES = KNOWN_TEXT.encode('ascii')
KNOWN_LEN = len(KNOWN_BYTES)


def decrypt_vigenere(cipher, key):
    #Дешифрует сообщение шифром Вижинера
    decrypted = []
    key_len = len(key)
    for i in range(len(cipher)):
        d = (cipher[i] - key[i % key_len]) % 256
        decrypted.append(d)
    return bytes(decrypted)


def is_valid_key(key):
    #проверяет, состоит ли ключ из нулей
    # Ключ не должен быть [0] или содержать только нули
    if all(k == 0 for k in key):
        return False
    # Ключ не должен быть слишком простым
    if len(key) == 1 and key[0] < 5:
        return False
    return True


def main():
    # Читаем зашифрованные данные
    data = read_data_1byte("text1_vigener_c.txt")

    # Приводим к bytes
    if isinstance(data, list):
        cipher = bytes(data)
    elif isinstance(data, bytes):
        cipher = data
    else:
        cipher = data.encode('ascii')

    n = len(cipher)

    print(f"Длина шифртекста: {n}")
    print(f"Длина известного текста '{KNOWN_TEXT}': {KNOWN_LEN}")
    print("-" * 60)

    found_solutions = []

    # Перебираем возможные длины ключа
    for key_len in range(1, 31):  # Увеличивваем до 30
        print(f"\nПроверка длины ключа: {key_len}")

        # Перебираем возможные позиции
        max_shifts = min(500, n - KNOWN_LEN + 1)  # Увеличиваем до 500

        for shift in range(max_shifts):
            segment = cipher[shift:shift + KNOWN_LEN]
            # Вычисляем фрагмент ключа
            key_fragment = []
            for i in range(KNOWN_LEN):
                k = (segment[i] - KNOWN_BYTES[i]) % 256
                key_fragment.append(k)
            # Формируем полный ключ
            if len(key_fragment) >= key_len:
                key = key_fragment[:key_len]
            else:
                key = (key_fragment * ((key_len // len(key_fragment)) + 1))[:key_len]

            #проверяем, что ключ не тривиальный
            if not is_valid_key(key):
                continue
            #дешифруем
            decrypted_bytes = decrypt_vigenere(cipher, key)

            # Пробуем декодировать в строку
            try:
                decrypted_text = decrypted_bytes.decode('ascii', errors='strict')
            except:
                try:
                    decrypted_text = decrypted_bytes.decode('latin-1', errors='ignore')
                except:
                    continue

            # Проверяем, что известная фраза действительно есть в тексте
            if KNOWN_TEXT.lower() not in decrypted_text.lower():
                continue

            #проверяем большую часть текста, а не только начало
            # Берем первые 1000 символов или весь текст если он короче
            check_length = min(1000, len(decrypted_text))
            text_to_check = decrypted_text[:check_length]

            # Увеличиваем требования к английскому тексту
            if detectEnglish.isEnglish(text_to_check, wordPercentage=40, letterPercentage=85):
                printable_chars = sum(1 for c in decrypted_text if c.isprintable() or c in '\n\r\t')
                printable_ratio = printable_chars / len(decrypted_text) if decrypted_text else 0

                if printable_ratio < 0.85:  #если меньше 85 проц печатаемых символов - пропускаем
                    continue

                found_solutions.append((key, shift, key_len, decrypted_text))

                print("-" * 60)
                print("НАЙДЕНО РЕШЕНИЕ!")
                print(f"Длина ключа: {key_len}")
                print(f"Позиция '{KNOWN_TEXT}': {shift}")
                print(f"Ключ (байты): {key}")
                key_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in key)
                print(f"Ключ (текст): {key_str}")
                print("-" * 60)
                print("Дешифрованный текст (первые 800 символов):")
                print(decrypted_text[:800])
                print("-" * 60)

    if found_solutions:
        # Выбираем лучшее решение (с самым длинным ключом)
        best_solution = max(found_solutions, key=lambda x: x[2])
        key, shift, key_len, decrypted_text = best_solution

        print("\n" + "=" * 60)
        print("ЛУЧШЕЕ РЕШЕНИЕ:")
        print(f"Ключ: {''.join(chr(b) if 32 <= b < 127 else '.' for b in key)}")
        print(f"Длина ключа: {key_len}")
        print(f"Позиция '{KNOWN_TEXT}': {shift}")
        print("=" * 60)

        # Сохраняем полный дешифрованный текст
        with open("text1_decrypted.txt", "w", encoding='utf-8') as f:
            f.write(decrypted_text)
        print("Полный текст сохранён в файл: text1_decrypted.txt")
    else:
        print("-" * 60)
        print("Не удалось автоматически найти решение.")
        print("Попробуйте увеличить диапазон длин ключа или количество сдвигов.")


if __name__ == "__main__":
    main()