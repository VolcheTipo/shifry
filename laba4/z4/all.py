# all.py
# Демонстрация режимов блочного шифрования на примере простого шифра Цезаря (побайтово)
# + универсальные функции для работы с любым блочным шифром.

def caesar_encrypt(byte_val, key):
    return (byte_val + key) % 256

def caesar_decrypt(byte_val, key):
    return (byte_val - key) % 256

def xor_byte(b1, b2):
    return b1 ^ b2

# ----- Универсальные функции для блочных шифров (добавлены без изменения старых) -----
def ecb_block(data, encrypt_block, decrypt_block, block_size=2, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    for i in range(skip_bytes, len(data), block_size):
        if i + block_size <= len(data):
            block = 0
            for j in range(block_size):
                block = (block << 8) | data[i + j]
            processed = encrypt_block(block) if encrypt else decrypt_block(block)
            for j in range(block_size - 1, -1, -1):
                result.append((processed >> (8 * j)) & 0xFF)
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def cbc_block(data, encrypt_block, decrypt_block, iv, block_size=2, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    prev = iv
    for i in range(skip_bytes, len(data), block_size):
        if i + block_size <= len(data):
            block = 0
            for j in range(block_size):
                block = (block << 8) | data[i + j]
            if encrypt:
                xored = block ^ prev
                processed = encrypt_block(xored)
                result.extend(processed.to_bytes(block_size, 'big'))
                prev = processed
            else:
                dec = decrypt_block(block)
                xored = dec ^ prev
                result.extend(xored.to_bytes(block_size, 'big'))
                prev = block
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def ofb_block(data, encrypt_block, iv, block_size=2, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data), block_size):
        if i + block_size <= len(data):
            register = encrypt_block(register)
            keystream = register
            block = 0
            for j in range(block_size):
                block = (block << 8) | data[i + j]
            processed = block ^ keystream
            result.extend(processed.to_bytes(block_size, 'big'))
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def cfb_block(data, encrypt_block, iv, block_size=2, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data), block_size):
        if i + block_size <= len(data):
            keystream = encrypt_block(register)
            block = 0
            for j in range(block_size):
                block = (block << 8) | data[i + j]
            processed = block ^ keystream
            result.extend(processed.to_bytes(block_size, 'big'))
            register = processed if encrypt else block
        else:
            result.extend(data[i:])
            break
    return bytes(result)

def ctr_block(data, encrypt_block, iv, block_size=2, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    counter = iv
    for i in range(skip_bytes, len(data), block_size):
        if i + block_size <= len(data):
            keystream = encrypt_block(counter)
            block = 0
            for j in range(block_size):
                block = (block << 8) | data[i + j]
            processed = block ^ keystream
            result.extend(processed.to_bytes(block_size, 'big'))
            counter = (counter + 1) & ((1 << (8 * block_size)) - 1)
        else:
            result.extend(data[i:])
            break
    return bytes(result)

# ----- Исходные функции для побайтового шифра Цезаря (без изменений) -----
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
            inp = xor_byte(b, prev)
            res = caesar_encrypt(inp, key)
            result.append(res)
            prev = res
        else:
            dec = caesar_decrypt(b, key)
            res = xor_byte(dec, prev)
            result.append(res)
            prev = b
    return bytes(result)

def ofb(data, key, iv, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data)):
        register = caesar_encrypt(register, key)
        keystream = register
        b = data[i]
        res = xor_byte(b, keystream)
        result.append(res)
    return bytes(result)

def cfb(data, key, iv, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    register = iv
    for i in range(skip_bytes, len(data)):
        keystream = caesar_encrypt(register, key)
        b = data[i]
        res = xor_byte(b, keystream)
        result.append(res)
        if encrypt:
            register = res
        else:
            register = b
    return bytes(result)

def ctr(data, key, iv, encrypt=True, skip_bytes=0):
    result = bytearray()
    result.extend(data[:skip_bytes])
    counter = iv
    for i in range(skip_bytes, len(data)):
        keystream = caesar_encrypt(counter, key)
        b = data[i]
        res = xor_byte(b, keystream)
        result.append(res)
        counter = (counter + 1) % 256
    return bytes(result)