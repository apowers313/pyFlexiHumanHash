from __future__ import annotations

from bitarray import bitarray
from bitarray.util import ba2int
import uuid
import math

class RandomSource:
    def __init__(self, b: bytes) -> None:
        self.bytes = b
        # print("bytes", b)
        self.ba = bitarray(buffer=b) # .reverse()?
        self.curr_offset = 0

    def get_bits(self, num_bits: int) -> int:
        start = self.curr_offset
        end = self.curr_offset + num_bits
        bits = self.ba[start:end]
        # print("bits", bits)
        self.curr_offset += num_bits
        return ba2int(bits)

    def get_max(self, max: int) -> int:
        num_bits = required_bits(max)
        res = self.get_bits(num_bits)
        # print(f"max: {max}; num_bits: {num_bits}, res: {res}")
        return res % max

    @staticmethod
    def from_uuid(u: uuid.UUID | str) -> RandomSource:
        if isinstance(u, str):
            u = uuid.UUID(u)
        return RandomSource(u.bytes)

    # from_hash(alg: str, alg_opts)
    # from_rand(nbytes: int = 16)

def required_bits(n: int) -> int:
    return math.ceil(math.log2(n))

def required_bytes(bits: int) -> int:
    return math.ceil(bits / 8)