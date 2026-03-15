def caesar_encrypt_byte(byte_val, key):
    return (byte_val + key) % 256

def xor_bytes(b1, b2):
    return b1 ^ b2

def mode_ecb(data, key, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    for i in range(skip_bytes, len(data)):
        b = data[i]
        if encrypt:
            res = caesar_encrypt_byte(b, key)
        else:
            res = (b - key) % 256
        result.append(res)
    return bytes(result)

def mode_ctr(data, key, iv, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    counter = iv
    for i in range(skip_bytes, len(data)):
        keystream = caesar_encrypt_byte(counter, key)
        res = xor_bytes(data[i], keystream)
        result.append(res)
        counter = (counter + 1) % 256
    return bytes(result)

def main():
    input_file = 'z3_caesar_ctr_c_all.bmp'
    key = 223
    iv = 78
    skip_bytes = 50

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        decrypted = mode_ctr(data, key, iv, skip_bytes=0)
        with open('z3_ctr_decrypted.bmp', 'wb') as f:
            f.write(decrypted)
        print("✓ Расшифровка CTR выполнена -> z3_ctr_decrypted.bmp")

        encrypted_ecb = mode_ecb(decrypted, key, encrypt=True, skip_bytes=skip_bytes)
        with open('z3_ctr_reencrypted_ecb.bmp', 'wb') as f:
            f.write(encrypted_ecb)
        print("✓ Шифрование ECB выполнено -> z3_ctr_reencrypted_ecb.bmp")

        encrypted_ctr = mode_ctr(decrypted, key, iv, skip_bytes=skip_bytes)
        with open('z3_ctr_reencrypted_ctr.bmp', 'wb') as f:
            f.write(encrypted_ctr)
        print("✓ Шифрование CTR выполнено -> z3_ctr_reencrypted_ctr.bmp")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()