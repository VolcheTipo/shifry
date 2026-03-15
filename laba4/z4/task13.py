
from spn1 import SPN1
SKIP_BYTES = 0
ROUNDS = 4
BLOCK_SIZE = 2

def ctr_decrypt_le(data, spn, rk, iv, rounds, skip_bytes):
    #CTR расшифровка с little-endian
    result = bytearray()
    result.extend(data[:skip_bytes])
    counter = iv
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            keystream = spn.encrypt(counter, rk, rounds)
            block = data[i] | (data[i + 1] << 8)
            plain = block ^ keystream
            result.append(plain & 0xFF)
            result.append((plain >> 8) & 0xFF)
            counter = (counter + 1) & 0xFFFF
        else:
            result.extend(data[i:])
            break
    return bytes(result)


def try_decrypt_with_key(data, spn, key, iv):
    rk = spn.round_keys(key)
    decrypted = ctr_decrypt_le(data, spn, rk, iv, ROUNDS, SKIP_BYTES)
    return decrypted

def main():
    iv = 552211
    known_bits_str = '0110101011010011100001111'  # 25 младших бит
    infile = 'im31_spn_c_ctr_all.bmp'

    with open(infile, 'rb') as f:
        data = f.read()
    print(f"Известно младших бит: {len(known_bits_str)}")
    print(f"Известные биты: {known_bits_str}")
    print(f"IV: {iv}")
    print(f"Исходная сигнатура: {data[:2].hex()}")
    # Преобразуем известные биты в число
    known_bits = int(known_bits_str, 2)
    unknown_bits_count = 32 - len(known_bits_str)
    print(f"\nПеребираем {unknown_bits_count} неизвестных бит...")
    print(f"Всего вариантов: {2 ** unknown_bits_count}")
    spn = SPN1()
    found_key = None
    # Перебор всех возможных значений неизвестных битов
    for i in range(2 ** unknown_bits_count):
        # Формируем полный 32-битный ключ
        key = (i << len(known_bits_str)) | known_bits
        # Пробуем расшифровать
        decrypted = try_decrypt_with_key(data, spn, key, iv)
        # Проверяем, получилась ли сигнатура BMP
        if decrypted[:2] == b'BM':
            print(f"\nНайден ключ: {key} (0x{key:08X})")
            print(f"Сигнатура: {decrypted[:2].hex()}")
            found_key = key
            # Сохраняем расшифрованный файл
            with open('im31_spn_dec.bmp', 'wb') as f:
                f.write(decrypted)
            print(f"Файл сохранен: im31_spn_dec.bmp")
            # Проверяем обратное шифрование
            rk = spn.round_keys(key)
            from task12 import ctr_encrypt_le
            encrypted = ctr_encrypt_le(decrypted, spn, rk, iv, ROUNDS, SKIP_BYTES+50)
            with open('im31_spn_enc.bmp', 'wb') as f:
                f.write(encrypted)
            print(f"Зашифрованный файл: im31_spn_enc.bmp")
            if encrypted == data:
                print("Зашифрованный файл совпадает с исходным")
            break
        # Прогресс
        if i % 100000 == 0 and i > 0:
            print(f"Проверено {i} из {2 ** unknown_bits_count}...")
    if found_key is None:
        print("\nКлюч не найден")
        print("Возможные причины:")
        print("Неверное количество известных битов")
        print("Неверный IV")
        print("Неверный режим шифрования")


if __name__ == '__main__':
    main()