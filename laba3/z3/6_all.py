# Шифрование одного изображения во всех режимах для сравнения
def caesar_encrypt(byte_val, key):
    return (byte_val + key) % 256

def xor_bytes(b1, b2):
    return b1 ^ b2

def ecb(data, key, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    for i in range(skip_bytes, len(data)):
        b = data[i]
        res = caesar_encrypt(b, key)
        result.append(res)
    return bytes(result)


def cbc(data, key, iv, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    prev_block = iv
    for i in range(skip_bytes, len(data)):
        b = data[i]
        input_val = xor_bytes(b, prev_block)
        res = caesar_encrypt(input_val, key)
        result.append(res)
        prev_block = res
    return bytes(result)


def ofb(data, key, iv, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data)):
        register = caesar_encrypt(register, key)
        keystream = register
        b = data[i]
        res = xor_bytes(b, keystream)
        result.append(res)
    return bytes(result)


def cfb(data, key, iv, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data)):
        keystream = caesar_encrypt(register, key)
        b = data[i]
        res = xor_bytes(b, keystream)
        result.append(res)
        register = res
    return bytes(result)


def ctr(data, key, iv, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    counter = iv
    for i in range(skip_bytes, len(data)):
        keystream = caesar_encrypt(counter, key)
        b = data[i]
        res = xor_bytes(b, keystream)
        result.append(res)
        counter = (counter + 1) % 256
    return bytes(result)


def main():
    # Используем расшифрованный файл из Задания 1
    input_file = 'husky.bmp'
    key = 223
    iv = 59
    skip_bytes = 50

    modes = {
        'ecb': ecb,
        'cbc': lambda d, k, i, s: cbc(d, k, i, s),
        'ofb': lambda d, k, i, s: ofb(d, k, i, s),
        'cfb': lambda d, k, i, s: cfb(d, k, i, s),
        'ctr': lambda d, k, i, s: ctr(d, k, i, s)
    }

    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        print(f"Шифрование файла {input_file} во всех режимах...\n")

        for name, func in modes.items():
            if name == 'ecb':
                encrypted = func(data, key, skip_bytes)
            else:
                encrypted = func(data, key, iv, skip_bytes)

            outname = f'task6_{name}.bmp'
            with open(outname, 'wb') as f:
                f.write(encrypted)
            print(f"Режим {name.upper()} сохранен -> {outname}")
        print("\nПроверьте файлы")

    except FileNotFoundError:
        print(f"Ошибка: Файл {input_file} не найден.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()