from __future__ import annotations

from bitarray import bitarray
from bitarray.util import ba2int
import uuid
import math

class RandomSource:
    def __init__(self, b: bytes) -> None:
        self.bytes = b
        # self.ba = deserialize(b)  # .reverse()?
        self.ba = bitarray(buffer=b)
        self.curr_offset = 0

    def get_bits(self, num_bits: int) -> int:
        start = self.curr_offset
        end = self.curr_offset + num_bits
        bits = self.ba[start:end]
        # print("bits", bits)
        self.curr_offset += num_bits
        return ba2int(bits)

    def get_max(self, max: int) -> int:
        num_bits = math.ceil(math.log2(max))
        # print("num_bits", num_bits)
        return self.get_bits(num_bits) % max

    @staticmethod
    def from_uuid(u: uuid.UUID | str) -> RandomSource:
        if isinstance(u, str):
            u = uuid.UUID(u)
        return RandomSource(u.bytes)

    # from_hash(alg: str, alg_opts)
    # from_rand(nbytes: int = 16)
