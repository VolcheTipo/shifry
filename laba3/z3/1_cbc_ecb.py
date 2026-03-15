# Расшифровка CBC + Сравнение с ECB
def caesar_encrypt(byte_val, key):
    return (byte_val + key) % 256

def caesar_decrypt(byte_val, key):
    return (byte_val - key) % 256

def ecb(data, key, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    for i in range(skip_bytes, len(data)):
        b = data[i]
        if encrypt:
            res = caesar_encrypt(b, key)
        else:
            res = caesar_decrypt(b, key)
        result.append(res)
    return bytes(result)

def cbc(data, key, iv, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    prev = iv
    for i in range(skip_bytes, len(data)):
        b = data[i]
        if encrypt:
            val = b ^ prev #xor
            res = caesar_encrypt(val, key)
            prev = res
        else:
            val = caesar_decrypt(b, key)
            res = val ^ prev #xor
            prev = b
        result.append(res)
    return bytes(result)

def main():
    input_file = 'z1_caesar_cbc_c_all.bmp'
    key = 223
    iv = 59
    skip_bytes = 50

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        # 1. Расшифровка CBC (полностью, без пропуска)
        decrypted = cbc(data, key, iv, encrypt=False, skip_bytes=0)
        with open('z1_cbc_decrypted.bmp', 'wb') as f:
            f.write(decrypted)
        print("Расшифровка CBC выполнена -> z1_cbc_decrypted.bmp")

        # 2. Шифрование ECB (с пропуском первых 50 байт)
        encrypted_ecb = ecb(decrypted, key, encrypt=True, skip_bytes=skip_bytes)
        with open('z1_cbc_reencrypted_ecb.bmp', 'wb') as f:
            f.write(encrypted_ecb)
        print("Шифрование ECB выполнено -> z1_cbc_reencrypted_ecb.bmp")

        # 3. Шифрование CBC (с пропуском первых 50 байт)
        encrypted_cbc = cbc(decrypted, key, iv, encrypt=True, skip_bytes=skip_bytes)
        with open('z1_cbc_reencrypted_cbc.bmp', 'wb') as f:
            f.write(encrypted_cbc)
        print("Шифрование CBC выполнено -> z1_cbc_reencrypted_cbc.bmp")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()