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
            # Генерируем гамму
            keystream = spn.encrypt(counter, rk, rounds)
            # Читаем блок в little-endian
            block = data[i] | (data[i + 1] << 8)
            # XOR с гаммой
            plain = block ^ keystream
            # Записываем в little-endian
            result.append(plain & 0xFF)
            result.append((plain >> 8) & 0xFF)
            # Инкремент счетчика
            counter = (counter + 1) & 0xFFFF
        else:
            result.extend(data[i:])
            break
    return bytes(result)


def ctr_encrypt_le(data, spn, rk, iv, rounds, skip_bytes):
    #CTR шифрование с little-endian
    skip_bytes += 50
    result = bytearray()
    result.extend(data[:skip_bytes])
    counter = iv
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            # Генерируем гамму
            keystream = spn.encrypt(counter, rk, rounds)
            # Читаем блок открытого текста
            block = data[i] | (data[i + 1] << 8)
            # XOR с гаммой
            enc = block ^ keystream
            # Записываем в little-endian
            result.append(enc & 0xFF)
            result.append((enc >> 8) & 0xFF)
            # Инкремент счетчика
            counter = (counter + 1) & 0xFFFF
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def main():
    key = 3136432567
    iv = 7546
    infile = 'im30_spn_c_ctr_all.bmp'
    with open(infile, 'rb') as f:
        data = f.read()
    print(f"Исходная сигнатура: {data[:2].hex()}")
    spn = SPN1()
    rk = spn.round_keys(key)
    # Расшифровка
    decrypted = ctr_decrypt_le(data, spn, rk, iv, ROUNDS, SKIP_BYTES)
    with open('im30_spn_dec.bmp', 'wb') as f:
        f.write(decrypted)
    print(f"Расшифрованная сигнатура: {decrypted[:2].hex()}")

    if decrypted[:2] == b'BM':
        print("Файл im30_spn_dec.bmp расшифрован!")
    else:
        print("сигнатура не BM")
    # Обратное шифрование
    encrypted = ctr_encrypt_le(decrypted, spn, rk, iv, ROUNDS, SKIP_BYTES)
    with open('im30_spn_enc.bmp', 'wb') as f:
        f.write(encrypted)
    print(f"Зашифрованная сигнатура: {encrypted[:2].hex()}")
    if encrypted == data:
        print("Зашифрованный файл совпадает с исходным!")
    else:
        print("Файлы не совпадают")


if __name__ == '__main__':
    main()