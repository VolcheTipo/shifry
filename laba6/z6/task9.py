from pathlib import Path
from sdes import SDes


class SDesExtended(SDes):
    def F(self, block, k):
        exp = self.ep(block) ^ k
        l4, r4 = self.divide_into_two(exp, 8)
        return self.p4(self.mux(self.s0(l4), self.s1(r4), 2))

    def f_k(self, block, SK):
        l, r = self.divide_into_two(block, 8)
        return self.mux(l ^ self.F(r, SK), r, 4)

    def sdes(self, block, k1, k2):
        return self.ipinv(self.f_k(self.sw(self.f_k(self.ip(block), k1)), k2))

    def key_schedule(self, key):
        k = self.p10(key)
        l, r = self.divide_into_two(k, 10)
        l1, r1 = self.ls1(l), self.ls1(r)
        self.k1 = self.p8(self.mux(l1, r1, 5))
        l2, r2 = self.ls2(l1), self.ls2(r1)
        self.k2 = self.p8(self.mux(l2, r2, 5))
        return self.k1, self.k2

    def encrypt(self, byte_value):
        return self.sdes(byte_value, self.k1, self.k2)

    def decrypt(self, byte_value):
        return self.sdes(byte_value, self.k2, self.k1)

    def process_ecb(self, data, key, decrypt=False):
        self.key_schedule(key)
        out = bytearray()
        for byte in data:
            out.append(self.decrypt(byte) if decrypt else self.encrypt(byte))
        return bytes(out)

    def process_cbc(self, data, key, iv, decrypt=False):
        self.key_schedule(key)
        out = bytearray()
        prev = iv & 0xFF
        for byte in data:
            if decrypt:
                plain = self.decrypt(byte) ^ prev
                out.append(plain)
                prev = byte
            else:
                cipher = self.encrypt(byte ^ prev)
                out.append(cipher)
                prev = cipher
        return bytes(out)

#Важно не запутаться с raw, payload, header (в плане где и что стоит в process_ecb, process_cbc и write_bites)!!!
def transform_bmp(input_path: str | Path, key: int, iv: int) -> tuple[Path, Path, Path]:
    input_path = Path(input_path)
    raw = input_path.read_bytes()
    header, payload = raw[:50], raw[50:]
    sdes = SDesExtended()
    decrypted_payload = sdes.process_cbc(raw, key, iv, decrypt=True)
    decrypted_path = input_path.with_name(f'{input_path.stem}_decrypted_cbc.bmp')
    decrypted_path.write_bytes(decrypted_payload)
    header = decrypted_payload[:50]
    encrypted_ecb = sdes.process_ecb(payload, key, decrypt=False)
    encrypted_ecb_path = input_path.with_name(f'{input_path.stem}_encrypted_ecb.bmp')
    encrypted_ecb_path.write_bytes(header + encrypted_ecb)
    encrypted_cbc = sdes.process_cbc(payload, key, iv, decrypt=False)
    encrypted_cbc_path = input_path.with_name(f'{input_path.stem}_encrypted_cbc.bmp')
    encrypted_cbc_path.write_bytes(header + encrypted_cbc)
    return decrypted_path, encrypted_ecb_path, encrypted_cbc_path


if __name__ == '__main__':
    source = Path('aa2_sdes_c_cbc_all.bmp')
    key = 845
    iv = 56
    if not source.exists():
        raise FileNotFoundError(f'Не найден файл: {source}')
    dec_path, ecb_path, cbc_path = transform_bmp(source, key, iv)
    print(f'Расшифрованный файл: {dec_path}')
    print(f'ECB-результат: {ecb_path}')
    print(f'CBC-результат: {cbc_path}')
