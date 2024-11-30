from flexihumanhash.rand import RandomSource

class TestRand:
    def test_get_bits(self) -> None:
        r = RandomSource(b"\x12")
        n = r.get_bits(8)
        assert n == 0x12

    def test_get_bits_multi(self) -> None:
        r = RandomSource(b"\x12")
        assert r.curr_offset == 0

        n1 = r.get_bits(4)
        assert r.curr_offset == 4
        assert n1 == 1

        n2 = r.get_bits(4)
        assert r.curr_offset == 8
        assert n2 == 2
    
    def test_get_max(self) -> None:
        r = RandomSource(b"\xAF")
        n = r.get_max(16)
        assert n == 0xA

        r = RandomSource(b"\xAF")
        n = r.get_max(4)
        assert n == 2

        r = RandomSource(b"\xAF")
        n = r.get_max(3)
        assert n == 2

        r = RandomSource(b"\xFF")
        n = r.get_max(12)
        assert n == 3
    
    def test_uuid_from_str(self) -> None:
        r = RandomSource.from_uuid("ae139e30-8021-459e-ab1a-034a29a1b8bb")
        n = r.get_bits(16)
        assert n == 0xae13