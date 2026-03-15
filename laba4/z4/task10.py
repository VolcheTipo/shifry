from spn1 import SPN1

SKIP_BYTES = 0
ROUNDS = 4
BLOCK_SIZE = 2


def ofb_decrypt_le(data, spn, rk, iv, rounds, skip_bytes):
    #OFB расшифровка с little-endian
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            register = spn.encrypt(register, rk, rounds)
            keystream = register
            # Читаем блок в little-endian
            block = data[i] | (data[i + 1] << 8)
            # XOR с гаммой
            plain = block ^ keystream
            # Записываем в little-endian
            result.append(plain & 0xFF)
            result.append((plain >> 8) & 0xFF)
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def ofb_encrypt_le(data, spn, rk, iv, rounds, skip_bytes):
    #OFB шифрование с little-endian
    skip_bytes += 50
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data), BLOCK_SIZE):
        if i + BLOCK_SIZE <= len(data):
            # Генерируем гамму
            register = spn.encrypt(register, rk, rounds)
            keystream = register
            # Читаем блок открытого текста
            block = data[i] | (data[i + 1] << 8)
            # XOR с гаммой
            enc = block ^ keystream
            # Записываем в little-endian
            result.append(enc & 0xFF)
            result.append((enc >> 8) & 0xFF)
        else:
            result.extend(data[i:])
            break

    return bytes(result)


def main():
    key = 898387587921
    iv = 3253
    infile = 'im28_spn_c_ofb_all.bmp'

    with open(infile, 'rb') as f:
        data = f.read()

    print(f"Исходная сигнатура: {data[:2].hex()}")

    spn = SPN1()
    rk = spn.round_keys(key)

    # Расшифровка
    decrypted = ofb_decrypt_le(data, spn, rk, iv, ROUNDS, SKIP_BYTES)

    with open('im28_spn_dec.bmp', 'wb') as f:
        f.write(decrypted)

    print(f"Расшифрованная сигнатура: {decrypted[:2].hex()}")

    if decrypted[:2] == b'BM':
        print("✅ УСПЕХ! Файл im28_spn_dec.bmp расшифрован!")
    else:
        print("❌ Ошибка: сигнатура не BM")

    # Обратное шифрование
    encrypted = ofb_encrypt_le(decrypted, spn, rk, iv, ROUNDS, SKIP_BYTES)

    with open('im28_spn_enc.bmp', 'wb') as f:
        f.write(encrypted)

    print(f"Зашифрованная сигнатура: {encrypted[:2].hex()}")

    if encrypted == data:
        print("✅ Зашифрованный файл совпадает с исходным!")
    else:
        print("⚠ Файлы не совпадают")


if __name__ == '__main__':
    main()