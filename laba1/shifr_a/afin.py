L = 256
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def find_mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None

    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1,
            u2 - q * v2,
            u3 - q * v3,
            v1, v2, v3
        )
    return u1 % m

def encrypt_byte(m, a, b):
    return (a * m + b) % L

def decrypt_byte(c, a, b):
    a_inv = find_mod_inverse(a, L)
    if a_inv is None:
        raise ValueError("a и L не взаимно простые")

    return (a_inv * ((c - b) % L)) % L

def encrypt_data(data, a, b, skip_bytes=0):
    result = []
    for i, m in enumerate(data):
        if i < skip_bytes:
            result.append(m)
        else:
            result.append(encrypt_byte(m, a, b))
    return result

def decrypt_data(data, a, b):
    result = []
    for c in data:
        result.append(decrypt_byte(c, a, b))
    return result

def read_bytes(filename):
    with open(filename, "rb") as f:
        return list(f.read())

def write_bytes(filename, data):
    with open(filename, "wb") as f:
        f.write(bytes(data))

data_enc = read_bytes("ff2_affine_c_all.bmp")
# сигнатура BMP
BMP_HEADER = [66, 77]  # 'BM'

count = 0
found = False

# перебор ключей
for a in range(1, 256):
    if gcd(a, 256) != 1:
        continue
    for b in range(256):
        count += 1
        # проверяем только первые два байта. Если это bmp файл, первые байты будут 66 в десятичной (42 в 16ной) и 77 в десятичной (4D в 16-ной)
        ok = True
        for i in range(2):
            m = decrypt_byte(data_enc[i], a, b)
            if m != BMP_HEADER[i]:
                ok = False
                break

        if ok:
            print("Ключ найден:")
            print("a =", a)
            print("b =", b)
            print("Перебрано ключей:", count)

            key_a = a
            key_b = b
            found = True
            break

    if found:
        break
if not found:
    print("Ключ не найден")
    exit()
# 1) расшифровать файл
data_dec = decrypt_data(data_enc, key_a, key_b)
write_bytes("ff2_decrypted.bmp", data_dec)
print("Файл расшифрован: ff2_decrypted.bmp")
# 2) зашифровать снова, оставив первые 50 байт
data_reenc = encrypt_data(data_dec, key_a, key_b, skip_bytes=50)
write_bytes("ff2_reencrypted.bmp", data_reenc)
print("Файл зашифрован снова: ff2_reencrypted.bmp")

if data_reenc == data_enc:
    print("Файлы совпадают")
else:
    print("Файлы НЕ совпадают")