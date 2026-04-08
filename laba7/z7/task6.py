from pathlib import Path
from saes import SAES

INPUT_FILE = Path("t20_saes_ctr_c_all.txt")
OUTPUT_FILE = Path("t20_saes_ctr_c_all_dec.txt")
IV = 2318
MIX_COLS = [['7', '3'], ['2', 'e']]
IRREDUCIBLE = 0b11111  # x^4 + x^3 + x^2 + x + 1


def main() -> None:
    saes = SAES(column_Matrix=MIX_COLS, modulus=IRREDUCIBLE)
    data = INPUT_FILE.read_bytes()

    #1) поиск ключа (Text Heuristic Attack)
    print("🔍 Поиск ключа полным перебором (0..65535)...")
    # Эвристика: текстовые файлы состоят из печатных символов, пробелов и переносов строк
    def is_text_byte(b):
        return 32 <= b <= 126 or 192 <= b <= 255 or b in (9, 10, 13, 32)
    check_blocks = min(len(data) // 2, 30)  # Проверяем первые примерно 60 байт
    found_key = None
    for k in range(65536):
        k0, k1, k2 = saes.key_expansion(k)
        valid = True
        for i in range(check_blocks):
            c_block = data[i * 2] | (data[i * 2 + 1] << 8)
            counter = (IV + i) & 0xFFFF
            keystream = saes.encrypt(counter, k0, k1, k2)
            p_block = c_block ^ keystream
            if not (is_text_byte(p_block & 0xFF) and is_text_byte((p_block >> 8) & 0xFF)):
                valid = False
                break
        if valid:
            found_key = k
            print(f" Ключ найден: {found_key} (0x{found_key:X})")
            break
    if found_key is None:
        raise ValueError("Ключ не найден. Проверьте входные данные или порядок байтов.")
    k0, k1, k2 = saes.key_expansion(found_key)
    # 2) расшифровка CTR =================
    print("Расшифровка файла...")
    dec_result = bytearray()
    counter = IV
    i = 0
    while i + 1 < len(data):
        c_block = data[i] | (data[i + 1] << 8)
        keystream = saes.encrypt(counter, k0, k1, k2)
        p_block = c_block ^ keystream
        dec_result.append(p_block & 0xFF)
        dec_result.append((p_block >> 8) & 0xFF)
        counter = (counter + 1) & 0xFFFF
        i += 2
    # Корректная обработка последнего нечётного байта (берём младший байт гаммы)
    if i < len(data):
        keystream = saes.encrypt(counter, k0, k1, k2)
        dec_result.append(data[i] ^ (keystream & 0xFF))
    OUTPUT_FILE.write_bytes(dec_result)
    print(f"Расшифровано: {OUTPUT_FILE}")
    # Предпросмотр результата
    try:
        # Пробуем декодировать как UTF-8, если не выходит — как CP1251 (Windows Cyrillic)
        text = dec_result.decode('utf-8')
    except UnicodeDecodeError:
        text = dec_result.decode('cp1251', errors='replace')
    print(" Первые 200 символов:")
    print(text[:200])
    print("Готово(УРААА)")


if __name__ == "__main__":
    main()