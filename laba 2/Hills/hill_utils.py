import math

#mod = 256 , тк работаем с картинками
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    # расширенный Евклид
    if gcd(a, m) != 1:
        return None  # Обратный не существует
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def matrix_det(matrix):
    # Определитель матрицы 2x2
    return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])


def matrix_inv_2x2(matrix, mod):
    # Находит обратную матрицу 2x2 по модулю
    det = matrix_det(matrix) % mod
    det_inv = mod_inverse(det, mod)

    if det_inv is None:
        raise ValueError(f"Определитель {det} не взаимно прост с {mod}. Обратной матрицы не существует.")

    # Формула обратной матрицы: det^(-1) * [[d, -b], [-c, a]]
    inv_matrix = [
        [(det_inv * matrix[1][1]) % mod, (det_inv * -matrix[0][1]) % mod],
        [(det_inv * -matrix[1][0]) % mod, (det_inv * matrix[0][0]) % mod]
    ]
    return inv_matrix


def matrix_mul_vec(matrix, vector, mod):
    # Умножение матрицы 2x2 на вектор 2x1 по модулю
    res = [
        (matrix[0][0] * vector[0] + matrix[0][1] * vector[1]) % mod,
        (matrix[1][0] * vector[0] + matrix[1][1] * vector[1]) % mod
    ]
    return res


def hill_encrypt(data_bytes, key_matrix, skip_bytes=0):
    # Шифрование байтов ключом 2x2
    result = bytearray()
    # Копируем первые байты без изменений
    result.extend(data_bytes[:skip_bytes])

    # Обрабатываем остальное блоками по 2 байта
    offset = skip_bytes
    # Если длина нечет, добавляем нулевой байт для выравнивания
    working_data = data_bytes[offset:]
    if len(working_data) % 2 != 0:
        working_data += b'\x00'

    for i in range(0, len(working_data), 2):
        block = [working_data[i], working_data[i + 1]]
        enc_block = matrix_mul_vec(key_matrix, block, 256)
        result.append(enc_block[0])
        result.append(enc_block[1])

    return bytes(result)


def hill_decrypt(data_bytes, key_matrix, skip_bytes=0):
    # Расшифровка байтов ключом
    mult_m = [] #проверка на ед матрицу (что: матрица * об матрица = ед матрица)
    inv_key = matrix_inv_2x2(key_matrix, 256)
    for i in range(4):
        mult_m.append((key_matrix[0][0]*inv_key[0][0] + key_matrix[0][1]*inv_key[1][0])%256)
        mult_m.append((key_matrix[0][0] * inv_key[0][1] + key_matrix[0][1]*inv_key[1][1])%256)
        mult_m.append((key_matrix[1][0] * inv_key[0][0] + key_matrix[1][1] * inv_key[1][0])%256)
        mult_m.append((key_matrix[1][0] * inv_key[0][1] + key_matrix[1][1] * inv_key[1][1])%256)
    print("spisik", mult_m)
    return hill_encrypt(data_bytes, inv_key, skip_bytes)


def recover_key(known_plain, known_cipher):
    #
    # Восстановление ключа 2x2 по известному открытому и шифртексту;
    # known_plain: 4 байта (2 блока); known_cipher: 4 байта (2 блока)
    #
    # Уравнение: C = K * P  =>  K = C * P_inv

    if len(known_plain) != 4 or len(known_cipher) != 4:
        raise ValueError("Нужно ровно 4 байта для восстановления ключа 2x2")

    # Формируем матрицы P и C из байтов
    # P = [[p1, p3], [p2, p4]]

    # пусть вектора
    p1, p2 = known_plain[0], known_plain[1]
    p3, p4 = known_plain[2], known_plain[3]

    c1, c2 = known_cipher[0], known_cipher[1]
    c3, c4 = known_cipher[2], known_cipher[3]

    # Матрица Plaintext (столбцы - вектора открытого текста)
    P = [[p1, p3], [p2, p4]]
    # Матрица Ciphertext
    C = [[c1, c3], [c2, c4]]

    try:
        P_inv = matrix_inv_2x2(P, 256)
        # K = C * P_inv
        k00 = (C[0][0] * P_inv[0][0] + C[0][1] * P_inv[1][0]) % 256
        k01 = (C[0][0] * P_inv[0][1] + C[0][1] * P_inv[1][1]) % 256
        k10 = (C[1][0] * P_inv[0][0] + C[1][1] * P_inv[1][0]) % 256
        k11 = (C[1][0] * P_inv[0][1] + C[1][1] * P_inv[1][1]) % 256

        return [[k00, k01], [k10, k11]]
    except ValueError:
        return None  # Не удалось найти обратную матрицу P