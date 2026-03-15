from spn1 import SPN1

SKIP_BYTES = 0
ROUNDS = 4
BLOCK_SIZE = 2
def cbc_decrypt_le(data, spn, lk, iv, rounds, skip_bytes):
    #CBC расшифровка с little-endian
    result = bytearray()
    result.extend(data[:skip_bytes])
    prev = iv
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            # Little-endian: младший байт первый
            block = data[i] | (data[i + 1] << 8)
            # Расшифровываем блок
            dec = spn.decrypt(block, lk, rounds)
            # XOR с предыдущим блоком шифртекста
            plain = dec ^ prev
            # Записываем в little-endian
            result.append(plain & 0xFF)
            result.append((plain >> 8) & 0xFF)
            # Обновляем prev = текущий зашифрованный блок
            prev = block
        else:
            result.extend(data[i:])
            break
    return bytes(result)


def cbc_encrypt_le(data, spn, rk, iv, rounds, skip_bytes):
    #CBC шифрование с little-endian
    skip_bytes+=50
    result = bytearray()
    result.extend(data[:skip_bytes])
    prev = iv
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            # Читаем блок открытого текста (little-endian)
            block = data[i] | (data[i + 1] << 8)
            # XOR с предыдущим блоком шифртекста
            xored = block ^ prev
            # Шифруем
            enc = spn.encrypt(xored, rk, rounds)
            # Записываем в little-endian
            result.append(enc & 0xFF)
            result.append((enc >> 8) & 0xFF)
            # Обновляем prev = текущий зашифрованный блок
            prev = enc
        else:
            result.extend(data[i:])
            break
    return bytes(result)


def main():
    key = 345238754631
    iv = 9
    infile = 'd9_spn_c_cbc_all.bmp'
    with open(infile, 'rb') as f:
        data = f.read()
    print(f"Исходная сигнатура: {data[:2].hex()}")
    spn = SPN1()
    lk = spn.round_keys_to_decrypt(key)
    rk = spn.round_keys(key)
    # Расшифровка
    decrypted = cbc_decrypt_le(data, spn, lk, iv, ROUNDS, SKIP_BYTES)
    with open('d9_spn_dec.bmp', 'wb') as f:
        f.write(decrypted)
    print(f"Расшифрованная сигнатура: {decrypted[:2].hex()}")

    if decrypted[:2] == b'BM':
        print("Файл d9_spn_dec.bmp расшифрован")
    else:
        print("Ошибка: сигнатура не BM")
    # Обратное шифрование
    encrypted = cbc_encrypt_le(decrypted, spn, rk, iv, ROUNDS, SKIP_BYTES)
    with open('d9_spn_enc.bmp', 'wb') as f:
        f.write(encrypted)
    print(f"Зашифрованная сигнатура: {encrypted[:2].hex()}")
    # Проверка совпадения с исходником
    if encrypted == data:
        print("Зашифрованный файл совпадает с исходным")
    else:
        print("Файлы не совпадают")


if __name__ == '__main__':
    main()