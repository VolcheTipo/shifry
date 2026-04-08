from pathlib import Path
from saes import SAES

# Параметры
INPUT_FILE = Path("dd8_saes_ofb_c_all.bmp")
OUTPUT_DEC_FILE = Path("dd8_saes_ofb_c_all_dec.bmp")
OUTPUT_ENC_FILE = Path("dd8_saes_ofb_c_all_enc.bmp")
HEADER_SIZE = 50
KEY = 12345
IV = 5171
MIX_COLS = [['5', '3'], ['2', 'c']]
IRREDUCIBLE = 0b11111  # x^4 + x^3 + x^2 + x + 1


def main() -> None:
    # 1. Инициализация SAES
    saes = SAES(column_Matrix=MIX_COLS, modulus=IRREDUCIBLE)
    # 2. Расширение ключа (вызываем один раз)
    k0, k1, k2 = saes.key_expansion(KEY)
    data = INPUT_FILE.read_bytes()
    #1) расшифровка OFB (весь файл, Little-Endian)
    print("Расшифровка файла (OFB)")
    dec_result = bytearray()
    state = IV  # В OFB состояние (генератор гаммы) инициализируется вектором IV
    i = 0
    while i + 1 < len(data):
        # Little-Endian: первый байт — младший (LSB), второй — старший (MSB)
        cipher_block = data[i] | (data[i + 1] << 8)
        # Генерируем блок гаммы: шифруем текущее состояние
        state = saes.encrypt(state, k0, k1, k2)
        # XOR гаммы с шифротекстом даёт открытый текст
        plain_block = cipher_block ^ state
        # Записываем в Little-Endian порядке
        dec_result.append(plain_block & 0xFF)
        dec_result.append((plain_block >> 8) & 0xFF)
        i += 2
    # Если длина файла нечётная, последний байт копируем как есть
    if i < len(data):
        dec_result.append(data[i])
    OUTPUT_DEC_FILE.write_bytes(dec_result)
    print(f"Расшифровано: {OUTPUT_DEC_FILE}")
    print(f"Сигнатура: {dec_result[0]:02X} {dec_result[1]:02X} (ожидалось 42 4D)")
    # 2) шифрование OFB (пропуск 50 байт, Little-Endian)
    print("\n Шифрование в режиме OFB")
    # Копируем заголовок без изменений
    enc_result = bytearray(dec_result[:HEADER_SIZE])
    state = IV  # Сбрасываем состояние гаммы для шифрования
    i = HEADER_SIZE
    while i + 1 < len(dec_result):
        # Little-Endian чтение
        plain_block = dec_result[i] | (dec_result[i + 1] << 8)
        # Генерируем блок гаммы
        state = saes.encrypt(state, k0, k1, k2)
        # XOR открытого текста с гаммой даёт шифротекст
        cipher_block = plain_block ^ state
        # Записываем в Little-Endian порядке
        enc_result.append(cipher_block & 0xFF)
        enc_result.append((cipher_block >> 8) & 0xFF)
        i += 2
    if i < len(dec_result):
        enc_result.append(dec_result[i])
    OUTPUT_ENC_FILE.write_bytes(enc_result)
    print(f"Зашифровано: {OUTPUT_ENC_FILE}")
    print(f"Заголовок сохранён: {enc_result[0]:02X} {enc_result[1]:02X}")
    print("Готово(УРААА)")


if __name__ == "__main__":
    main()