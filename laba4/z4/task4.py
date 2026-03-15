import spn1

def task4():
    #round_keys_to_decrypt()
    e = spn1.SPN1()
    k = 734533245
    lk = e.round_keys_to_decrypt(k)
    print(f'Ключи расшифрования для K={k}:')
    for i, l in enumerate(lk):
        print(f'L{i} = {bin(l)[2:].zfill(16)}\n')


if __name__ == "__main__":
    task4()