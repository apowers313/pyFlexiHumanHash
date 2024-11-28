from flexihumanhash import FlexiHumanHash
from jinja2 import Environment, BaseLoader

class TestHash:
    def test_exists(self) -> None:
        FlexiHumanHash("")

    def test_noun(self) -> None:
        fhh = FlexiHumanHash("{{noun}}-{{foo}}")
        print("fhh required vars", fhh.vars)
        ret = fhh.hash(b"Hello World")
        print("ret", ret)

    # def test_deleteme(self) -> None:
    #     env: Environment = Environment(loader=BaseLoader)  # type: ignore
    #     ast = env.parse("{{foo}}-{{bar}}-{{bas(x=42)}}")
    #     print("ast", ast.body[0].nodes[4].node.name)
    #     print("ast", ast.body[0].nodes)
    #     # [Name(name='foo', ctx='load'), TemplateData(data='-'), Name(name='bar', ctx='load')]