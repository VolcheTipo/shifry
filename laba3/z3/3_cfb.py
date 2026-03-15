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

def cfb(data, key, iv, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    reg = iv
    for i in range(skip_bytes, len(data)):
        keystream = caesar_encrypt(reg, key)
        b = data[i]
        res = xor_bytes(b, keystream)
        result.append(res)
        reg = res if encrypt else b
    return bytes(result)

def main():
    input_file = 'z2_caesar_cfb_c_all.bmp'
    key = 174
    iv = 9
    skip_bytes = 50

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        # Расшифровка CFB (полностью)
        decrypted = cfb(data, key, iv, encrypt=False, skip_bytes=0)
        with open('z2_cfb_decrypted.bmp', 'wb') as f:
            f.write(decrypted)
        print("Расшифровка CFB выполнена -> z2_cfb_decrypted.bmp")

        # Шифрование ECB (с пропуском первых 50 байт)
        encrypted_ecb = ecb(decrypted, key, encrypt=True, skip_bytes=skip_bytes)
        with open('z2_cfb_reencrypted_ecb.bmp', 'wb') as f:
            f.write(encrypted_ecb)
        print("Шифрование ECB выполнено -> z2_cfb_reencrypted_ecb.bmp")

        # Шифрование CFB (с пропуском первых 50 байт)
        encrypted_cfb = cfb(decrypted, key, iv, encrypt=True, skip_bytes=skip_bytes)
        with open('z2_cfb_reencrypted_cfb.bmp', 'wb') as f:
            f.write(encrypted_cfb)
        print("Шифрование CFB выполнено -> z2_cfb_reencrypted_cfb.bmp")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()