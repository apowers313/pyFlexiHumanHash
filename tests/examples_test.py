from flexihumanhash import FlexiHumanHash

class TestExamples:
    def test_basic(self) -> None:
        fhh = FlexiHumanHash("{{adj}}-{{noun}}")
        ret = fhh.hash("hello world")
        assert str(ret) == "crookedest-valentines"
        ret = fhh.hash(31337)
        assert str(ret) == "worthiest-omelettes"
        ret = fhh.hash(bytes([0, 1, 3, 5]))
        assert str(ret) == "manila-dive"

    def test_basic2(self) -> None:
        fhh = FlexiHumanHash("{{adj}}-{{adj}}-{{noun}}-{{decimal(4)}}")
        ret = fhh.hash("hello world.")
        assert str(ret) == "manuscript-anatomically-naps-5303"

    def test_rand(self) -> None:
        fhh = FlexiHumanHash("{{adj}}, {{adj}} {{noun}} {{hex(4)}}")
        print(fhh.rand())
        # Expected output: "stalwart, dominant attire f214"