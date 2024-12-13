from flexihumanhash.rand import RandomSource


class TestRand:
    def test_get_max_multi(self) -> None:
        r = RandomSource(b"\x12")
        assert r.big_num == 18

        n1 = r.get_max(4)
        assert r.big_num == 4
        assert n1 == 2

        n2 = r.get_max(4)
        assert r.big_num == 1
        assert n2 == 0

        n3 = r.get_max(4)
        assert r.big_num == 0
        assert n3 == 1

        n4 = r.get_max(4)
        assert r.big_num == 0
        assert n4 == 0

    def test_get_max(self) -> None:
        r = RandomSource(b"\xaf")
        n = r.get_max(16)
        assert n == 15

        r = RandomSource(b"\xaf")
        n = r.get_max(4)
        assert n == 3

        r = RandomSource(b"\xaf")
        n = r.get_max(3)
        assert n == 1

        r = RandomSource(b"\xff")
        n = r.get_max(12)
        assert n == 3

    def test_uuid_from_str(self) -> None:
        r = RandomSource.from_uuid("ae139e30-8021-459e-ab1a-034a29a1b8bb")
        n = r.get_max(16)
        assert n == 11
