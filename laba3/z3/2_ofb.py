def caesar_encrypt(byte_val, key):
    return (byte_val + key) % 256

def caesar_decrypt(byte_val, key):
    return (byte_val - key) % 256

def xor_bytes(b1, b2):
    return b1 ^ b2

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

def ofb(data, key, iv, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    reg = iv
    for i in range(skip_bytes, len(data)):
        reg = caesar_encrypt(reg, key)
        keystream = reg
        res = xor_bytes(data[i], keystream)
        result.append(res)
    return bytes(result)

def main():
    input_file = 'im8_caesar_ofb_c_all.bmp'
    key = 56
    iv = 9
    skip_bytes = 50

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        # 1. Расшифровка OFB
        decrypted = ofb(data, key, iv, encrypt=False, skip_bytes=0)
        with open('im8_ofb_decrypted.bmp', 'wb') as f:
            f.write(decrypted)
        print("Расшифровка OFB выполнена -> im8_ofb_decrypted.bmp")
        # 2. Шифрование ECB (с пропуском первых 50 байт)
        encrypted_ecb = ecb(decrypted, key, encrypt=True, skip_bytes=skip_bytes)
        with open('im8_ofb_reencrypted_ecb.bmp', 'wb') as f:
            f.write(encrypted_ecb)
        print("Шифрование ECB выполнено -> im8_ofb_reencrypted_ecb.bmp")
        # 3. Шифрование OFB (с пропуском первых 50 байт)
        encrypted_ofb = ofb(decrypted, key, iv, encrypt=True, skip_bytes=skip_bytes)
        with open('im8_ofb_reencrypted_ofb.bmp', 'wb') as f:
            f.write(encrypted_ofb)
        print("Шифрование OFB выполнено -> im8_ofb_reencrypted_ofb.bmp")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()