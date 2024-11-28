from jinja2 import Environment, BaseLoader
from jinja2.nodes import Name, TemplateData, Call
from typing import Any
import warnings


class JinjaExpr:
    def __call__(self, *args: Any, **kwargs: dict[str, Any]) -> str:
        return ""

    def __str__(self) -> str:
        return ""

jinja_expressions: dict[str, JinjaExpr] = {}

class FlexiHumanHash:
    def __init__(self, template: str) -> None:
        self.template_str = template
        self.jinja_env: Environment = Environment(loader=BaseLoader) # type: ignore
        self.jinja_env.globals.update(jinja_expressions)
        self.jinja_template = self.jinja_env.from_string(self.template_str)

        # find order of variables in template, used for calculating required entropy
        vars: list[str] = []
        unexpected = False
        self.ast = self.jinja_env.parse(self.template_str)
        if len(self.ast.body) != 1:
            unexpected = True
        for n in self.ast.body[0].nodes: # type: ignore
            match n:
                case Name():
                    vars.append(n.name)
                case Call():
                    vars.append(n.node.name) # type: ignore
                case TemplateData():
                    continue
                case _:
                    unexpected = True

        if unexpected:
            warnings.warn("Unexpected template format")
        self.vars = vars

    def hash(self, data: bytes, *, ctx: dict[str, Any] = dict()) -> str:
        return self.jinja_template.render(**ctx)
    
    def hash_str(self, data: str) -> str:
        return ""

    def hash_int(self, data: int) -> str:
        return ""