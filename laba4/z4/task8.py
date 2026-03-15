from spn1 import SPN1

SKIP_BYTES = 0
ROUNDS = 4
BLOCK_SIZE = 2

def ecb_decrypt_le(data, spn, lk, rounds, skip_bytes):
    #ECB расшифровка с little-endian (как в BMP)
    result = bytearray()
    result.extend(data[:skip_bytes])
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            # Little-endian: младший байт первый
            block = data[i] | (data[i + 1] << 8)
            # Расшифровываем
            decrypted = spn.decrypt(block, lk, rounds)
            # Записываем в little-endian
            result.append(decrypted & 0xFF)
            result.append((decrypted >> 8) & 0xFF)
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def ecb_encrypt_le(data, spn, rk, rounds, skip_bytes):
    #ECB шифрование с little-endian
    skip_bytes+=50
    result = bytearray()
    result.extend(data[:skip_bytes])

    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            # Little-endian
            block = data[i] | (data[i + 1] << 8)
            # Шифруем
            encrypted = spn.encrypt(block, rk, rounds)
            # Записываем в little-endian
            result.append(encrypted & 0xFF)
            result.append((encrypted >> 8) & 0xFF)
        else:
            result.extend(data[i:])
            break
    return bytes(result)


def main():
    key = 34523456231
    infile = 'd5_spn_c_all.bmp'
    with open(infile, 'rb') as f:
        data = f.read()
    print(f"Исходная сигнатура: {data[:2].hex()}")
    spn = SPN1()
    lk = spn.round_keys_to_decrypt(key)
    rk = spn.round_keys(key)
    # Расшифровка
    decrypted = ecb_decrypt_le(data, spn, lk, ROUNDS, SKIP_BYTES)
    with open('d5_spn_dec.bmp', 'wb') as f:
        f.write(decrypted)
    print(f"Расшифрованная сигнатура: {decrypted[:2].hex()}")
    if decrypted[:2] == b'BM':
        print("Файл d5_spn_dec.bmp расшифрован")
    else:
        print("Ошибка")
    # Обратное шифрование (проверка)
    encrypted = ecb_encrypt_le(decrypted, spn, rk, ROUNDS, SKIP_BYTES)
    with open('d5_spn_enc.bmp', 'wb') as f:
        f.write(encrypted)
    print(f"Зашифрованная сигнатура: {encrypted[:2].hex()}")
    # Проверка совпадения с исходником
    if encrypted == data:
        print("Зашифрованный файл совпадает с исходным")
    else:
        print("Файлы не совпадают")


if __name__ == '__main__':
    main()