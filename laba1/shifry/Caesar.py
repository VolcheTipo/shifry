def encrypt(m, key):
    c = (m + key) % 256
    return c

def decrypt(m, key):
    c = (m - key) % 256
    return c

def encrypt_data(data, key):
    cypher_data = []
    for m in data:
        c = encrypt(m, key)
        cypher_data.append(c)
    return cypher_data

def decrypt_data(data_c, key):
    data = []
    for c in data_c:
        m = decrypt(c, key)
        data.append(m)
    return data