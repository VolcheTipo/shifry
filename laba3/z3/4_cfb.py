def caesar_encrypt(byte_val, key):
    return (byte_val + key) % 256

def ecb(data, key, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    for i in range(skip_bytes, len(data)):
        b = data[i]
        if encrypt:
            res = caesar_encrypt(b, key)
        else:
            res = (b - key) % 256
        result.append(res)
    return bytes(result)

def cfb_3bit(data, key, iv, encrypt=True, skip_bytes=0):
    header = data[:skip_bytes]
    payload = data[skip_bytes:]

    bits = []
    for byte in payload:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    result_bits = []
    register = iv & 0xFF
    i = 0
    while i < len(bits):
        r = min(3, len(bits) - i)
        input_bits = bits[i:i + r]

        keystream = caesar_encrypt(register, key)
        ks = [(keystream >> 7) & 1, (keystream >> 6) & 1, (keystream >> 5) & 1]

        out_bits = [input_bits[k] ^ ks[k] for k in range(r)]

        feedback = out_bits if encrypt else input_bits
        register = ((register << r) & 0xFF)
        val = 0
        for k in range(r):
            if feedback[k]:
                val |= (1 << (r - 1 - k))
        register |= val

        result_bits.extend(out_bits)
        i += r

    result_payload = bytearray()
    for j in range(0, len(result_bits), 8):
        byte = 0
        for k in range(8):
            byte = (byte << 1) | (result_bits[j + k] if j + k < len(result_bits) else 0)
        result_payload.append(byte)

    return header + bytes(result_payload)

def main():
    input_file = 'm1_caesar_cfb_3bit_c_all.bmp'
    key = 174
    iv = 59
    skip_bytes = 50

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        decrypted = cfb_3bit(data, key, iv, encrypt=False, skip_bytes=0)
        with open('m1_cfb_3bit_decrypted.bmp', 'wb') as f:
            f.write(decrypted)
        print("Расшифровка CFB 3-bit выполнена -> m1_cfb_3bit_decrypted.bmp")

        encrypted_ecb = ecb(decrypted, key, encrypt=True, skip_bytes=skip_bytes)
        with open('m1_cfb_3bit_reencrypted_ecb.bmp', 'wb') as f:
            f.write(encrypted_ecb)
        print("Шифрование ECB выполнено -> m1_cfb_3bit_reencrypted_ecb.bmp")

        encrypted_cfb = cfb_3bit(decrypted, key, iv, encrypt=True, skip_bytes=skip_bytes)
        with open('m1_cfb_3bit_reencrypted_cfb.bmp', 'wb') as f:
            f.write(encrypted_cfb)
        print("Шифрование CFB 3-bit выполнено -> m1_cfb_3bit_reencrypted_cfb.bmp")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()