from flexihumanhash import FlexiHumanHash
import pytest


class TestHash:
    def test_exists(self) -> None:
        FlexiHumanHash("")

    def test_init(self) -> None:
        fhh = FlexiHumanHash(
            "{{noun}}-{{verb()}}-{{adj(min=4, max=5)}}-{{decimal(size=6)}}-{{hex(5)}}"
        )
        assert len(fhh.call_records) == 5
        assert fhh.call_records[0].name == "noun"
        assert fhh.call_records[0].args == ()
        assert fhh.call_records[0].kwargs == {}
        assert fhh.call_records[1].name == "verb"
        assert fhh.call_records[1].args == ()
        assert fhh.call_records[1].kwargs == {}
        assert fhh.call_records[2].name == "adj"
        assert fhh.call_records[2].args == ()
        assert fhh.call_records[2].kwargs == {"min": 4, "max": 5}
        assert fhh.call_records[3].name == "decimal"
        assert fhh.call_records[3].args == ()
        assert fhh.call_records[3].kwargs == {"size": 6}
        assert fhh.call_records[4].name == "hex"
        assert fhh.call_records[4].args == (5,)
        assert fhh.call_records[4].kwargs == {}

    def test_underflow(self) -> None:
        fhh = FlexiHumanHash("{{noun}}")
        ret = fhh.from_bytes(b"\x0f")

        assert len(ret.input) == 1
        assert len(ret.data) == 2
        assert ret.bits_provided == 8
        assert ret.bits_used == 16

    def test_noun(self) -> None:
        fhh = FlexiHumanHash("{{noun}}")
        assert fhh.entropy == 47004
        assert fhh.entropy_bits == 16
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "aardvark"

    def test_noun_uppercase(self) -> None:
        fhh = FlexiHumanHash("{{noun|upper}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "AARDVARK"

    def test_noun_capitalize(self) -> None:
        fhh = FlexiHumanHash("{{noun|capitalize}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "Aardvark"

    def test_noun_len(self) -> None:
        fhh = FlexiHumanHash("{{noun(min=4, max=5)}}")
        assert fhh.entropy == 6407
        assert fhh.entropy_bits == 13
        assert fhh.call_records[0].name == "noun"
        assert fhh.call_records[0].dict.size == 6407

    def test_adj(self) -> None:
        fhh = FlexiHumanHash("{{adj}}")
        assert fhh.entropy == 14903
        assert fhh.entropy_bits == 14
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "aback"

    def test_verb(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        assert fhh.entropy == 31232
        assert fhh.entropy_bits == 15
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "abandon"

    def test_entropy(self) -> None:
        fhh = FlexiHumanHash("{{noun}} {{verb}} {{adj}}")
        assert fhh.entropy == 21878035113984  # 47004 * 14903 * 31232
        assert fhh.entropy_bits == 45  # 14 + 15 + 16

    def test_hex(self) -> None:
        fhh = FlexiHumanHash("{{hex}}")
        ret = fhh.from_bytes(b"\xaa\x11\x00\xff")
        assert fhh.call_records[0].name == "hex"
        assert fhh.call_records[0].dict.size == 65536
        assert str(ret) == "aa11"

    def test_hex_len(self) -> None:
        fhh = FlexiHumanHash("{{hex(8)}}")
        ret = fhh.from_bytes(b"\xaa\x11\x00\xff")
        assert fhh.call_records[0].name == "hex"
        assert fhh.call_records[0].dict.size == 4294967296
        assert str(ret) == "aa1100ff"

    def test_decimal(self) -> None:
        fhh = FlexiHumanHash("{{decimal}}")
        ret = fhh.from_bytes(b"\xff\xff\xff\xff\xff\xff")
        assert fhh.call_records[0].name == "decimal"
        assert fhh.call_records[0].dict.size == 10000
        assert str(ret) == "6383"  # log2(10000) = 14; 2^14 = 16383; 16383 % 10000 = 6383

    def test_city(self) -> None:
        fhh = FlexiHumanHash("{{city}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "El Tarter"

    def test_first_name(self) -> None:
        fhh = FlexiHumanHash("{{firstname}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "Aaren"

    def test_first_name_lower(self) -> None:
        fhh = FlexiHumanHash("{{firstname|lower}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "aaren"

    def test_last_name(self) -> None:
        fhh = FlexiHumanHash("{{lastname}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "Aaberg"

    def test_female_name(self) -> None:
        fhh = FlexiHumanHash("{{femalename}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "Aaren"

    def test_male_name(self) -> None:
        fhh = FlexiHumanHash("{{malename}}")
        ret = fhh.from_bytes(b"\x00\x00\x00\x00")
        assert str(ret) == "Aaron"

    def test_combo(self) -> None:
        fhh = FlexiHumanHash(
            "{{hex(2)}} {{firstname}} {{lastname}} from {{city}} is a {{adj}} {{noun}} who ran to the {{noun}} {{decimal}}"
        )
        ret = fhh.from_bytes(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        assert (
            str(ret)
            == "00 Aaren Aaberg from El Tarter is a aback aardvark who ran to the aardvark 0000"
        )

    def test_rand(self) -> None:
        fhh = FlexiHumanHash("{{adj}}")
        res = fhh.rand()

        assert res.input_source == "rand"
        assert res.bits_provided == 16
        assert res.bits_used == 14

    def test_hash(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World")

        assert str(res) == "appease"
        assert res.data == b"\x06\xc6"
        assert res.input_source == "hash:blake2b:2"
        assert res.bits_provided == 16
        assert res.bits_used == 15
        assert res.entropy == 31232

    def test_unknown_hash(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        with pytest.raises(TypeError, match="unknown hash algorithm: foo"):
            fhh.hash("Hello World", alg="foo")

    def test_hash_shake_128(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="shake128")

        assert str(res) == "bivouacking"
        assert res.data == b"\x12\x27"
        assert res.input_source == "hash:shake128:2"
        assert res.bits_provided == 16
        assert res.bits_used == 15

    def test_hash_shake256(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="shake256")

        assert str(res) == "moped"
        assert res.data == b"\x84\x0d"
        assert res.input_source == "hash:shake256:2"
        assert res.bits_provided == 16
        assert res.bits_used == 15

    def test_hash_md5(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="md5")

        assert str(res) == "resembles"
        assert res.data == b"\xb1\x0a\x8d\xb1\x64\xe0\x75\x41\x05\xb7\xa9\x9b\xe7\x2e\x3f\xe5"
        assert res.input_source == "hash:md5"
        assert res.bits_provided == 128
        assert res.bits_used == 15

    def test_hash_sha1(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha1")

        assert str(res) == "awakened"
        assert (
            res.data
            == b"\x0a\x4d\x55\xa8\xd7\x78\xe5\x02\x2f\xab\x70\x19\x77\xc5\xd8\x40\xbb\xc4\x86\xd0"
        )
        assert res.input_source == "hash:sha1"
        assert res.bits_provided == 160
        assert res.bits_used == 15

    def test_hash_sha224(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha224")

        assert str(res) == "skyjacking"
        assert (
            res.data
            == b"\xc4\x89\x0f\xaf\xfd\xb0\x10\x5d\x99\x1a\x46\x1e\x66\x8e\x27\x66\x85\x40\x1b\x02\xea\xb1\xef\x43\x72\x79\x50\x47"
        )
        assert res.input_source == "hash:sha224"
        assert res.bits_provided == 224
        assert res.bits_used == 15

    def test_hash_sha256(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha256")

        assert str(res) == "react"
        assert (
            res.data
            == b"\xa5\x91\xa6\xd4\x0b\xf4\x20\x40\x4a\x01\x17\x33\xcf\xb7\xb1\x90\xd6\x2c\x65\xbf\x0b\xcd\xa3\x2b\x57\xb2\x77\xd9\xad\x9f\x14\x6e"
        )
        assert res.input_source == "hash:sha256"
        assert res.bits_provided == 256
        assert res.bits_used == 15

    def test_hash_sha384(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha384")

        assert str(res) == "pluralize"
        assert (
            res.data
            == b"\x99\x51\x43\x29\x18\x6b\x2f\x6a\xe4\xa1\x32\x9e\x7e\xe6\xc6\x10\xa7\x29\x63\x63\x35\x17\x4a\xc6\xb7\x40\xf9\x02\x83\x96\xfc\xc8\x03\xd0\xe9\x38\x63\xa7\xc3\xd9\x0f\x86\xbe\xee\x78\x2f\x4f\x3f"
        )
        assert res.input_source == "hash:sha384"
        assert res.bits_provided == 384
        assert res.bits_used == 15

    def test_hash_sha512(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha512")

        assert str(res) == "coquette"
        assert (
            res.data
            == b"\x2c\x74\xfd\x17\xed\xaf\xd8\x0e\x84\x47\xb0\xd4\x67\x41\xee\x24\x3b\x7e\xb7\x4d\xd2\x14\x9a\x0a\xb1\xb9\x24\x6f\xb3\x03\x82\xf2\x7e\x85\x3d\x85\x85\x71\x9e\x0e\x67\xcb\xda\x0d\xaa\x8f\x51\x67\x10\x64\x61\x5d\x64\x5a\xe2\x7a\xcb\x15\xbf\xb1\x44\x7f\x45\x9b"
        )
        assert res.input_source == "hash:sha512"
        assert res.bits_provided == 512
        assert res.bits_used == 15

    def test_hash_sha3_224(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha3-224")

        assert str(res) == "overhanging"
        assert (
            res.data
            == b"\x8e\x80\x00\x79\xa0\xb3\x11\x78\x8b\xf2\x93\x53\xf4\x00\xef\xf9\x69\xb6\x50\xa3\x59\x7c\x91\xef\xd9\xaa\x5b\x38"
        )
        assert res.input_source == "hash:sha3-224"
        assert res.bits_provided == 224
        assert res.bits_used == 15

    def test_hash_sha3_256(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha3-256")

        assert str(res) == "trolled"
        assert (
            res.data
            == b"\xe1\x67\xf6\x8d\x65\x63\xd7\x5b\xb2\x5f\x3a\xa4\x9c\x29\xef\x61\x2d\x41\x35\x2d\xc0\x06\x06\xde\x7c\xbd\x63\x0b\xb2\x66\x5f\x51"
        )
        assert res.input_source == "hash:sha3-256"
        assert res.bits_provided == 256
        assert res.bits_used == 15

    def test_hash_sha3_384(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha3-384")

        assert str(res) == "reciprocates"
        assert (
            res.data
            == b"\xa7\x8e\xc2\x85\x1e\x99\x16\x38\xce\x50\x5d\x4a\x44\xef\xa6\x06\xdd\x40\x56\xd3\xab\x27\x4e\xc6\xfd\xba\xc0\x0c\xde\x16\x47\x82\x63\xef\x72\x13\xba\xd5\xa7\xdb\x70\x44\xf5\x8d\x63\x7a\xfd\xeb"
        )
        assert res.input_source == "hash:sha3-384"
        assert res.bits_provided == 384
        assert res.bits_used == 15

    def test_hash_sha3_512(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        res = fhh.hash("Hello World", alg="sha3-512")

        assert str(res) == "disincline"
        assert (
            res.data
            == b"\x3d\x58\xa7\x19\xc6\x86\x6b\x02\x14\xf9\x6b\x0a\x67\xb3\x7e\x51\xa9\x1e\x23\x3c\xe0\xbe\x12\x6a\x08\xf3\x5f\xdf\x4c\x04\x3c\x61\x26\xf4\x01\x39\xbf\xbc\x33\x8d\x44\xeb\x2a\x03\xde\x9f\x7b\xb8\xef\xf0\xac\x26\x0b\x36\x29\x81\x1e\x38\x9a\x5f\xbe\xe8\xa8\x94"
        )
        assert res.input_source == "hash:sha3-512"
        assert res.bits_provided == 512
        assert res.bits_used == 15

    def test_hash_blake2s(self) -> None:
        fhh = FlexiHumanHash("{{noun}}")
        res = fhh.hash("Hello World", alg="blake2s")

        assert str(res) == "liabilities"
        assert res.hasher is fhh
        assert res.data == b"\x5c\x83"
        assert res.input_data == b"\x5c\x83"
        assert res.input == "Hello World"
        assert res.input_source == "hash:blake2s:2"
        assert res.bits_provided == 16
        assert res.bits_used == 16
        assert res.entropy == 47004

    def test_hash_longer_blake2s(self) -> None:
        fhh = FlexiHumanHash("{{firstname}}-{{lastname}}-the-{{adj}}-{{noun}}")
        res = fhh.hash("hello world...", alg="blake2s")

        assert str(res) == "Tamarah-Hebbe-the-grossest-masonry"
        assert res.data == b"\xd1\x47\xc6\x3a\x93\xcc\x58\x68"
        assert res.input_source == "hash:blake2s:8"
        assert res.bits_provided == 64
        assert res.bits_used == 59
