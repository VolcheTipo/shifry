from collections import Counter
import os
import sys
import detectEnglish
import read_write_file as _rw

MAX_KEYLEN = 60  # можно увеличить, если ожидается длинный ключ
TOP_N_COMMON = 3  # если основной вариант не сработает, можно попробовать из топ-N (упрощённая локальная доработка)


def read_cipher_bytes(fname: str) -> bytes:
    #Читает файл в байтах
    if _rw is not None and hasattr(_rw, 'read_data_1byte'):
        try:
            data = _rw.read_data_1byte(fname)
            if isinstance(data, (bytes, bytearray)):
                return bytes(data)
            if isinstance(data, list):
                return bytes(data)
            if isinstance(data, str):
                return data.encode('latin-1')
            return bytes(data)
        except Exception:
            pass
    with open(fname, 'rb') as f:
        return f.read()

def write_plain_bytes(fname: str, data: bytes):
    if _rw is not None and hasattr(_rw, 'write_data_1byte'):
        try:
            _rw.write_data_1byte(fname, data)
            return
        except Exception:
            pass
    with open(fname, 'wb') as f:
        f.write(data)

def decrypt_with_key(cipher: bytes, key: bytes) -> bytes:
    klen = len(key)
    if klen == 0:
        return cipher
    out = bytearray(len(cipher))
    for i, cb in enumerate(cipher):
        kb = key[i % klen]
        out[i] = (cb - kb) & 0xFF  # инвариант  C = (P + K) mod 256 -> P = (C - K) mod 256
    return bytes(out)

def score_english_text(candidate_bytes: bytes) -> float:
    """
    Возвращает оценку "англоязычности" для варианта
    Используем detectEnglish: он работает с Python str, поэтому декодируем bytes в latin-1
    Возвращаем 1.0 если isEnglish True, иначе долю совпадающих слов (через getEnglishCount).
    """
    s = candidate_bytes.decode('latin-1')
    try:
        if detectEnglish.isEnglish(s):
            return 1.0
    except Exception:
        pass

    try:
        cnt = detectEnglish.getEnglishCount(s)
        return float(cnt)
    except Exception:
        letters_only = detectEnglish.removeNonLetters(s) if hasattr(detectEnglish, 'removeNonLetters') else ''.join(ch for ch in s if ch.isalpha() or ch.isspace())
        if len(s) == 0:
            return 0.0
        return float(len(letters_only)) / len(s)

def guess_key_for_length(cipher: bytes, keylen: int) -> bytes:
    #наиболее частый байт в колонке соответствует пробелу (0x20)
    key_bytes = bytearray(keylen)
    n = len(cipher)
    for r in range(keylen):
        col = cipher[r:n:keylen]  # байты для этой позиции ключа
        if len(col) == 0:
            key_bytes[r] = 0
            continue
        freq = Counter(col)
        most_common_byte, _ = freq.most_common(1)[0]
        guessed_kb = (most_common_byte - 0x20) & 0xFF
        key_bytes[r] = guessed_kb
    return bytes(key_bytes)

def try_keylen_candidates(cipher: bytes, max_keylen: int):
    best = {'score': -1.0, 'key': b'', 'plain': b'', 'keylen': 0}
    founds = []
    for k in range(1, max_keylen + 1):
        key_guess = guess_key_for_length(cipher, k)
        plain = decrypt_with_key(cipher, key_guess)
        score = score_english_text(plain)
        # сохранить лучший
        if score > best['score']:
            best.update({'score': score, 'key': key_guess, 'plain': plain, 'keylen': k})
        # если detectEnglish полностью подтвердил, вернуть сразу
        # (score==1.0 означает detectEnglish.isEnglish сработал)
        if score >= 1.0:
            print(f"[+] Найден корректный ключ длины {k}")
            founds.append((k, key_guess, plain, score))
            # не break — возможно есть короткий ключ и лучший результат; но можно вернуть первый
            return founds, best
        # небольшая подсказка пользователю
        if k % 5 == 0 or k == 1:
            print(f"Пробовал длину ключа {k:02d}, текущий best score={best['score']:.4f}")
    return founds, best

def pretty_key_repr(key: bytes) -> str:
    #если байты печатаемые ascii, покажем строку, иначе hex
    try:
        text = key.decode('ascii')
        if all(32 <= ord(ch) < 127 for ch in text):
            return f"ascii: '{text}'"
    except Exception:
        pass
    return 'hex: ' + key.hex()

def main():
    cipher_fname = 'text4_vigener_c_all.txt'
    if not os.path.exists(cipher_fname):
        print(f"Файл {cipher_fname} не найден в текущей директории {os.getcwd()}")
        sys.exit(1)
    cipher = read_cipher_bytes(cipher_fname)
    print(f"Прочитано {len(cipher)} байт из {cipher_fname}.")

    print("Запускаю поиск ключа: частотный анализ; пробел - самый частый символ в колонках.")
    founds, best = try_keylen_candidates(cipher, MAX_KEYLEN)

    if founds:
        # Если найдено достоверное расшифрование, выводим и сохраняем первый
        k, key_bytes, plain_bytes, score = founds[0]
        print(f"\n=== Успех! Ключ длины {k} ===")
        print("Ключ:", pretty_key_repr(key_bytes))
        print(f"Оценка (score) = {score}")
        out_fname = 'text4_vigener_decrypted2.txt'
        write_plain_bytes(out_fname, plain_bytes)
        print(f"Расшифрованный текст сохранён в {out_fname}")
        s = plain_bytes.decode('latin-1', errors='replace')
        print("\nПервые 1500 символов расшифровки:\n")
        print(s[:1500])
        return


    print("\nНе найдено однозначного подтверждения через detectEnglish.isEnglish().")
    print(f"Лучший: ключ длины {best['keylen']}, score={best['score']:.4f}")
    print("Ключ (догадка):", pretty_key_repr(best['key']))
    s = best['plain'].decode('latin-1', errors='replace') #latin-1 чтобы не потерять информацию
    print("\nПервые 1500 символов лучшего:\n")
    print(s[:1500])


if __name__ == '__main__':
    main()