from pathlib import Path
from saes import SAES
# Настройки
KEY = 834
MIX_COLS = [['1', '4'], ['4', '1']]
IRREDUCIBLE = 0b10011
INPUT_ENC_FILE = Path("dd1_saes_c_all.bmp")
OUTPUT_DEC_FILE = Path("dd1_saes_c_all_dec.bmp")
OUTPUT_RE_ENC_FILE = Path("dd1_saes_c_all_enc.bmp")  # Результат повторного шифрования
HEADER_SIZE = 50


def main():
    saes = SAES(column_Matrix=MIX_COLS, modulus=IRREDUCIBLE)
    k0, k1, k2 = saes.key_expansion(KEY)
    #1) расшифровка (весь файл, Little-Endian)
    print("Начало расшифровки")
    enc_data = INPUT_ENC_FILE.read_bytes()
    dec_result = bytearray()
    i = 0
    while i + 1 < len(enc_data):
        # Little-Endian: data[i] — младший байт (LSB), data[i+1] — старший (MSB)
        block = enc_data[i] | (enc_data[i + 1] << 8)
        # Дешифруем блок
        decrypted_block = saes.decrypt(block, k0, k1, k2)
        # Записываем обратно в Little-Endian порядке
        dec_result.append(decrypted_block & 0xFF)  # LSB
        dec_result.append((decrypted_block >> 8) & 0xFF)  # MSB
        i += 2
    if i < len(enc_data):
        dec_result.append(enc_data[i])
    OUTPUT_DEC_FILE.write_bytes(dec_result)
    print(f"Расшифровано: {OUTPUT_DEC_FILE}")
    print(f"Сигнатура: {dec_result[0]:02X} {dec_result[1]:02X} (ожидалось 42 4D)")
    #2) шифрование (ECB, пропуск 50 байт, Little-Endian)
    print("\n Начало шифрования (ECB, пропуск первых 50 байт)...")
    dec_data = OUTPUT_DEC_FILE.read_bytes()
    enc_result = bytearray()
    #  Копируем заголовок без изменений
    enc_result.extend(dec_data[:HEADER_SIZE])
    #  Шифруем оставшиеся данные
    i = HEADER_SIZE
    while i + 1 < len(dec_data):
        # Little-Endian порядок
        block = dec_data[i] | (dec_data[i + 1] << 8)
        # Шифруем блок
        encrypted_block = saes.encrypt(block, k0, k1, k2)
        # Записываем в Little-Endian порядке
        enc_result.append(encrypted_block & 0xFF)  # LSB
        enc_result.append((encrypted_block >> 8) & 0xFF)  # MSB
        i += 2
    if i < len(dec_data):
        enc_result.append(dec_data[i])
    OUTPUT_RE_ENC_FILE.write_bytes(enc_result)
    print(f"Зашифровано: {OUTPUT_RE_ENC_FILE}")
    print(f"Заголовок сохранён: {enc_result[0]:02X} {enc_result[1]:02X}")
    print(f"Первые байты зашифрованной части: {enc_result[50]:02X} {enc_result[51]:02X}")
    print("Готово(УРААА)")


if __name__ == "__main__":
    main()