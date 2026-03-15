from read_write_file import read_data_1byte

WORD = "housewives"
WORD_BYTES = WORD.encode('ascii')
WORD_LEN = len(WORD_BYTES)


def main():
    # Читаем зашифрованные данные с помощью вашей внешней функции
    data = read_data_1byte("text4_vigener_c_all.txt")

    # Приводим к bytes для удобства работы с индексами
    if isinstance(data, list):
        cipher = bytes(data)
    elif isinstance(data, bytes):
        cipher = data
    else:
        cipher = data.encode('ascii')

    n = len(cipher)

    # Проверка на случай, если файл слишком короткий
    if n < WORD_LEN:
        print("Ошибка: Файл слишком короткий для поиска слова.")
        return

    print(f"Длина шифртекста: {n}")
    print(f"Длина слова '{WORD}': {WORD_LEN}")
    print("-" * 60)
    print("Формат: Shift [номер сдвига]: [предполагаемый фрагмент ключа]")
    print("Ищите строку, где текст читается (это и есть ключ)")
    print("-" * 60)

    # Перебираем все возможные сдвиги (от 0 до конца файла)
    # Задание: "Взять len значений... сдвиг на одно... сдвиг на два и т.д."
    for shift in range(n - WORD_LEN + 1):
        # Берем фрагмент шифртекста длиной с наше слово
        segment = cipher[shift:shift + WORD_LEN]

        # Вычитаем численные значения слова housewives
        key_fragment = []
        for i in range(WORD_LEN):
            # Формула Вижинера для ключа: K = (C - P) mod 256
            k = (segment[i] - WORD_BYTES[i]) % 256
            key_fragment.append(k)

        # Представляем полученные 10 значений в виде текста
        key_str = ''
        for b in key_fragment:
            # Оставляем только печатаемые ASCII символы для наглядности
            if 32 <= b < 127:
                key_str += chr(b)
            else:
                key_str += '.'

        # Печатаем результат для визуального поиска ключевого выражения
        print(f"Shift {shift:4d}: {key_str}")


if __name__ == "__main__":
    main()