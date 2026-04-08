from pathlib import Path
from saes import SAES

# Параметры
INPUT_FILE = Path("dd5_saes_cbc_c_all.bmp")
OUTPUT_DEC_FILE = Path("dd5_saes_cbc_c_all_dec.bmp")
OUTPUT_ENC_FILE = Path("dd5_saes_cbc_c_all_enc.bmp")
HEADER_SIZE = 50
KEY = 10217
IV = 456
MIX_COLS = [['a', 'c'], ['8', '6']]
IRREDUCIBLE = 0b11001  # x^4 + x^3 + 1


def main() -> None:
    #Инициализация SAES
    saes = SAES(column_Matrix=MIX_COLS, modulus=IRREDUCIBLE)
    #Расширение ключа
    k0, k1, k2 = saes.key_expansion(KEY)
    data = INPUT_FILE.read_bytes()

    #1) расшифровка CBC (весь файл, Little-Endian)
    print("Расшифровка файла (CBC)")
    dec_result = bytearray()
    prev = IV  # В CBC расшифровки prev = предыдущий блок шифротекста (или IV для первого)
    i = 0
    while i + 1 < len(data):
        # Little-Endian: первый байт — младший (LSB), второй — старший (MSB)
        cipher_block = data[i] | (data[i + 1] << 8)
        # Дешифруем блок
        decrypted_block = saes.decrypt(cipher_block, k0, k1, k2)
        # XOR с предыдущим блоком шифротекста (или IV)
        plain_block = decrypted_block ^ prev
        # Обновляем prev для следующего шага (в CBC это текущий шифротекст)
        prev = cipher_block
        # Записываем в Little-Endian порядке
        dec_result.append(plain_block & 0xFF)
        dec_result.append((plain_block >> 8) & 0xFF)
        i += 2
    if i < len(data):
        dec_result.append(data[i])
    OUTPUT_DEC_FILE.write_bytes(dec_result)
    print(f"Расшифровано: {OUTPUT_DEC_FILE}")
    print(f"Сигнатура: {dec_result[0]:02X} {dec_result[1]:02X} (ожидалось 42 4D)")

    #2) шифрование CBC (пропуск 50 байт, Little-Endian)
    print("\n Шифрование в режиме CBC ")
    enc_result = bytearray(dec_result[:HEADER_SIZE])  # Копируем заголовок без изменений
    prev = IV  # Сбрасываем IV для шифрования
    i = HEADER_SIZE
    while i + 1 < len(dec_result):
        # Little-Endian чтение
        plain_block = dec_result[i] | (dec_result[i + 1] << 8)
        # XOR с предыдущим блоком шифротекста (или IV)
        xored_block = plain_block ^ prev
        # Шифруем результат XOR
        cipher_block = saes.encrypt(xored_block, k0, k1, k2)
        # Обновляем prev (в CBC это текущий шифротекст)
        prev = cipher_block
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