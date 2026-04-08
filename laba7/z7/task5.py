from pathlib import Path
from saes import SAES

INPUT_FILE = Path("dd10_saes_cfb_c_all.bmp")
OUTPUT_DEC_FILE = Path("dd10_saes_cfb_c_all_dec.bmp")
OUTPUT_ENC_FILE = Path("dd10_saes_cfb_c_all_enc.bmp")
HEADER_SIZE = 50
IV = 9165
MIX_COLS = [['7', 'd'], ['4', '5']]
IRREDUCIBLE = 0b11001  # x^4 + x^3 + 1


def main() -> None:
    saes = SAES(column_Matrix=MIX_COLS, modulus=IRREDUCIBLE)
    data = INPUT_FILE.read_bytes()
    # 1) поиск ключа (Known-Plaintext Attack)
    # BMP всегда начинается с сигнатуры 'BM' -> байты 0x42, 0x4D.
    # В Little-Endian порядке это 16-битное число 0x4D42 (19778).
    P0 = 0x4D42
    C0 = IV  # IV в CFB выступает как C_(-1)
    C1 = data[0] | (data[1] << 8)  # Первый блок шифротекста
    # В CFB: C1 = P0 ^ E(K, C0)  =>  E(K, C0) = C1 ^ P0
    target_keystream = C1 ^ P0
    found_key = None
    print("Поиск ключа полным перебором (0..65535)")
    for k in range(65536):
        k0, k1, k2 = saes.key_expansion(k)
        # Шифруем IV текущим кандидатом ключа
        enc = saes.encrypt(C0, k0, k1, k2)
        if enc == target_keystream:
            found_key = k
            print(f" Ключ найден: {found_key} (0x{found_key:X})")
            break
    if found_key is None:
        raise ValueError("Ключ не найден. Проверьте входные данные и порядок байтов.")
    k0, k1, k2 = saes.key_expansion(found_key)

    # 2) расшифровка в режиме CFB
    print(" Расшифровка файла...")
    dec_result = bytearray()
    prev = C0  # В CFB prev хранит предыдущий блок шифротекста (или IV для первого блока)
    i = 0
    while i + 1 < len(data):
        cipher_block = data[i] | (data[i + 1] << 8)
        # CFB расшифровка: P_i = C_i ^ E(K, prev)
        # используется функция расшифрования!
        keystream = saes.encrypt(prev, k0, k1, k2)
        plain_block = cipher_block ^ keystream
        # Записываем в Little-Endian
        dec_result.append(plain_block & 0xFF)
        dec_result.append((plain_block >> 8) & 0xFF)
        # Обновляем цепочку: prev становится текущим блоком шифротекста
        prev = cipher_block
        i += 2
    if i < len(data):
        dec_result.append(data[i])
    OUTPUT_DEC_FILE.write_bytes(dec_result)
    print(f"Расшифровано: {OUTPUT_DEC_FILE}")
    print(f"Сигнатура: {dec_result[0]:02X} {dec_result[1]:02X} (ожидалось 42 4D)")
    # 3) шифр с пропуском 50б
    print("\n Шифрование в режиме CFB (пропуск первых 50 байт)...")
    # Копируем заголовок без изменений
    enc_result = bytearray(dec_result[:HEADER_SIZE])
    prev = IV  # Сбрасываем цепочку к IV
    i = HEADER_SIZE
    while i + 1 < len(dec_result):
        plain_block = dec_result[i] | (dec_result[i + 1] << 8)
        keystream = saes.encrypt(prev, k0, k1, k2)
        cipher_block = plain_block ^ keystream
        enc_result.append(cipher_block & 0xFF)
        enc_result.append((cipher_block >> 8) & 0xFF)
        prev = cipher_block
        i += 2
    if i < len(dec_result):
        enc_result.append(dec_result[i])
    OUTPUT_ENC_FILE.write_bytes(enc_result)
    print(f" Зашифровано: {OUTPUT_ENC_FILE}")
    print(f" Заголовок сохранён: {enc_result[0]:02X} {enc_result[1]:02X}")
    print(" Готово(УРАААА)")


if __name__ == "__main__":
    main()