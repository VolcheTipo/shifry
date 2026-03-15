import detectEnglish

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


def decrypt_byte(c, a, b):
    a_inv = find_mod_inverse(a, L)
    return (a_inv * ((c - b) % L)) % L


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

data_enc = read_bytes("text10_affine_c_all.txt")

count = 0
found = False

for a in range(1, 256):
    if gcd(a, 256) != 1:
        continue

    for b in range(256):
        count += 1

        test_bytes = []
        for i in range(min(300, len(data_enc))):
            test_bytes.append(decrypt_byte(data_enc[i], a, b))

        test_text = bytes(test_bytes).decode("ascii", errors="ignore")

        # если строка пустая — пропускаем
        if len(test_text) == 0:
            continue

        if detectEnglish.isEnglish(test_text):
            print("Ключ найден:")
            print("a =", a)
            print("b =", b)
            print("Перебрано ключей:", count)

            data_dec = decrypt_data(data_enc, a, b)
            write_bytes("text10_decrypted.txt", data_dec)

            found = True
            break

    if found:
        break

if not found:
    print("Ключ не найден")
    print("Перебрано ключей:", count)

# William Wordsworth (Уильям Вордсворт) Daffodils