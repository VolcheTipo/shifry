from pathlib import Path
from saes import SAES
# Параметры
INPUT_FILE = Path("bb02_saes_c_all.bmp")
OUTPUT_DEC_FILE = Path("bb02_saes_c_all_dec.bmp")
OUTPUT_ENC_FILE = Path("bb02_saes_c_all_enc.bmp")
HEADER_SIZE = 50
KEY = 2318
MIX_COLS = [['b', '4'], ['e', 'd']]
IRREDUCIBLE = 0b10011  # x^4 + x + 1

def main() -> None:
    #Инициализация SAES
    saes = SAES(column_Matrix=MIX_COLS, modulus=IRREDUCIBLE)
    #Расширение ключа
    k0, k1, k2 = saes.key_expansion(KEY)
    # 1) расшифровка (весь файл, Little-Endian)
    print("Расшифровка файла...")
    data = INPUT_FILE.read_bytes()
    dec_result = bytearray()
    i = 0
    while i + 1 < len(data):
        # Little-Endian: первый байт — младший (LSB), второй — старший (MSB)
        block = data[i] | (data[i + 1] << 8)
        # Дешифруем блок
        decrypted_block = saes.decrypt(block, k0, k1, k2)
        # Записываем обратно в Little-Endian порядке
        dec_result.append(decrypted_block & 0xFF)
        dec_result.append((decrypted_block >> 8) & 0xFF)
        i += 2
    # Если длина файла нечётная, последний байт копируем как есть
    if i < len(data):
        dec_result.append(data[i])
    OUTPUT_DEC_FILE.write_bytes(dec_result)
    print(f"Расшифровано: {OUTPUT_DEC_FILE}")
    print(f"Сигнатура: {dec_result[0]:02X} {dec_result[1]:02X} (ожидалось 42 4D)")
    #2) шифрование ECB (пропуск 50 байт, Little-Endian)
    print("\nШифрование в режиме ECB...")
    enc_result = bytearray()
    # Копируем заголовок без изменений
    enc_result.extend(dec_result[:HEADER_SIZE])
    i = HEADER_SIZE
    while i + 1 < len(dec_result):
        # Little-Endian порядок чтения
        block = dec_result[i] | (dec_result[i + 1] << 8)
        # Шифруем блок
        encrypted_block = saes.encrypt(block, k0, k1, k2)
        # Little-Endian порядок записи
        enc_result.append(encrypted_block & 0xFF)
        enc_result.append((encrypted_block >> 8) & 0xFF)
        i += 2
    if i < len(dec_result):
        enc_result.append(dec_result[i])

    OUTPUT_ENC_FILE.write_bytes(enc_result)
    print(f"Зашифровано: {OUTPUT_ENC_FILE}")
    print(f"Заголовок сохранён: {enc_result[0]:02X} {enc_result[1]:02X}")
    print("Готово(УРААА)")


if __name__ == "__main__":
    main()