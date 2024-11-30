from flexihumanhash import FlexiHumanHash
from jinja2 import Environment, BaseLoader

class TestHash:
    def test_exists(self) -> None:
        FlexiHumanHash("")

    def test_init(self) -> None:
        fhh = FlexiHumanHash("{{noun}}-{{verb()}}-{{adj(min=4, max=5)}}-{{decimal(size=6)}}-{{hex(5)}}")
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

    def test_noun(self) -> None:
        fhh = FlexiHumanHash("{{noun}}")
        ret = fhh.rand(b"\x00\x00\x00\x00")
        assert ret == "aardvark"

    def test_adj(self) -> None:
        fhh = FlexiHumanHash("{{adj}}")
        ret = fhh.rand(b"\x00\x00\x00\x00")
        assert ret == "aback"

    def test_verb(self) -> None:
        fhh = FlexiHumanHash("{{verb}}")
        ret = fhh.rand(b"\x00\x00\x00\x00")
        assert ret == "abandon"

    def test_noun_len(self) -> None:
        fhh = FlexiHumanHash("{{noun(min=4, max=5)}}")
        assert fhh.call_records[0].name == "noun"
        assert fhh.call_records[0].dict.size == 6407
