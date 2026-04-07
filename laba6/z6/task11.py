from pathlib import Path
from sdes import SDes


class SDesMITM(SDes):
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

    def encrypt_single(self, byte_value, key):
        self.key_schedule(key)
        return self.sdes(byte_value, self.k1, self.k2)

    def decrypt_single(self, byte_value, key):
        self.key_schedule(key)
        return self.sdes(byte_value, self.k2, self.k1)

    def double_encrypt(self, byte_value, first_key, second_key):
        return self.encrypt_single(self.encrypt_single(byte_value, first_key), second_key)

    def double_decrypt(self, byte_value, first_key, second_key):
        return self.decrypt_single(self.decrypt_single(byte_value, second_key), first_key)

    def _search_order(self, plaintext: bytes, ciphertext: bytes, first_is_k1: bool):
        if first_is_k1:
            # C = E_k2(E_k1(P))
            first_plain, first_cipher = plaintext[0], ciphertext[0]
            table = {}
            for k1 in range(1024):
                mid = self.encrypt_single(first_plain, k1)
                table.setdefault(mid, []).append(k1)
            candidates = []
            for k2 in range(1024):
                mid = self.decrypt_single(first_cipher, k2)
                for k1 in table.get(mid, []):
                    if all(self.double_encrypt(p, k1, k2) == c for p, c in zip(plaintext, ciphertext)):
                        candidates.append((k1, k2))
            return candidates

        # C = E_k1(E_k2(P))
        first_plain, first_cipher = plaintext[0], ciphertext[0]
        table = {}
        for k2 in range(1024):
            mid = self.encrypt_single(first_plain, k2)
            table.setdefault(mid, []).append(k2)
        candidates = []
        for k1 in range(1024):
            mid = self.decrypt_single(first_cipher, k1)
            for k2 in table.get(mid, []):
                if all(self.encrypt_single(self.encrypt_single(p, k2), k1) == c for p, c in zip(plaintext, ciphertext)):
                    candidates.append((k1, k2))
        return candidates

    def find_keys(self, ciphertext: bytes, known_plaintext: bytes):
        if len(ciphertext) < len(known_plaintext):
            raise ValueError('Ciphertext is shorter than the known plaintext')
        plaintext = known_plaintext[:8]
        ciphertext = ciphertext[:len(plaintext)]
        candidates = self._search_order(plaintext, ciphertext, first_is_k1=True)
        order = 'k1_then_k2'
        if not candidates:
            candidates = self._search_order(plaintext, ciphertext, first_is_k1=False)
            order = 'k2_then_k1'
        if not candidates:
            return None, None, None
        return candidates[0][0], candidates[0][1], order

    def decrypt_double_file(self, data: bytes, first_key: int, second_key: int, order: str = 'k1_then_k2') -> bytes:
        out = bytearray()
        if order == 'k1_then_k2':
            for byte in data:
                out.append(self.double_decrypt(byte, first_key, second_key))
        else:
            # Если шифрование было в обратном порядке.
            for byte in data:
                out.append(self.decrypt_single(self.decrypt_single(byte, first_key), second_key))
        return bytes(out)


def decrypt_png(input_path: str | Path) -> tuple[Path, int, int, str]:
    input_path = Path(input_path)
    raw = input_path.read_bytes()
    known_plain = b'\x89PNG\r\n\x1a\n'
    sdes = SDesMITM()
    k1, k2, order = sdes.find_keys(raw, known_plain)
    if k1 is None:
        raise RuntimeError('Не удалось восстановить ключи методом встречи посередине')
    decrypted = sdes.decrypt_double_file(raw, k1, k2, order=order)
    output_path = input_path.with_name(f'{input_path.stem}_decrypted.png')
    output_path.write_bytes(decrypted)
    return output_path, k1, k2, order


if __name__ == '__main__':
    source = Path('im50_sdes2k_c_all.png')
    if not source.exists():
        raise FileNotFoundError(f'Не найден файл: {source}')
    out_path, k1, k2, order = decrypt_png(source)
    print(f'Ключ 1: {k1}')
    print(f'Ключ 2: {k2}')
    print(f'Порядок: {order}')
    print(f'Расшифрованный файл: {out_path}')
