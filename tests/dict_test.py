from flexihumanhash.dict import FlexiTextDict, FlexiHexDict, FlexiDecimalDict, FlexiDict

class TestDict:
    def test_from_file(self) -> None:
        d = FlexiTextDict.from_file("nouns", "data/build/noun")
        assert d.get_entry(0) == "aardvark"

    def test_default_dicts(self) -> None:
        r = FlexiDict.get_registry()
        assert "city" in r
        assert r["city"].get_entry(0) == "El Tarter"
        assert "firstname" in r
        assert "lastname" in r
        assert "femalename" in r
        assert "malename" in r
        assert "noun" in r
        assert "adj" in r
        assert "verb" in r

class TestHex:
    def test_is_registered(self) -> None:
        r = FlexiDict.get_registry()
        assert "hex" in r
        d = r["hex"]
        assert d.get_entry(0) == "0000"

    def test_padding(self) -> None:
        d = FlexiHexDict(size=4)
        s = d.get_entry(10)
        assert s == "000a"
    
    def test_size(self) -> None:
        d = FlexiHexDict(size=4)
        assert d.size == 65536

class TestDecimal:
    def test_is_registered(self) -> None:
        r = FlexiDict.get_registry()
        assert "decimal" in r
        d = r["decimal"]
        assert d.get_entry(0) == "0000"

    def test_padding(self) -> None:
        d = FlexiDecimalDict(size=4)
        s = d.get_entry(10)
        assert s == "0010"
    
    def test_size(self) -> None:
        d = FlexiDecimalDict(size=4)
        assert d.size == 10000