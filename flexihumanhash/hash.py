from __future__ import annotations

from jinja2 import Environment, BaseLoader
from jinja2.nodes import Name, TemplateData, Call
from typing import Any
import os

from .dict import FlexiDict
from .rand import RandomSource


class FlexiHumanHash:
    def __init__(self, template: str) -> None:
        self.template_str = template
        self.jinja_env: Environment = Environment(loader=BaseLoader)  # type: ignore
        dicts = FlexiDict.get_registry()
        for dict_name in dicts.keys():
            self.jinja_env.globals[dict_name] = JinjaExpr(self, dict_name, dicts[dict_name])
        self.jinja_template = self.jinja_env.from_string(self.template_str)
        self.call_records: list[JinjaExpr] = []
        self.rndctx: RandomSource | None = None
        # XXX: when rndctx is None rendering the template has side-effects recording calls to calculate entropy
        self.jinja_template.render()

    def hash(self, data: bytes) -> str:
        return self.jinja_template.render()

    def hash_str(self, data: str) -> str:
        return ""

    def hash_int(self, data: int) -> str:
        return ""

    def rand(self, data: bytes | None = None, size: int = 16) -> str:
        if data is None:
            data = os.urandom(size)

        self.rndctx = RandomSource(data)
        ret = self.jinja_template.render()
        self.rndctx = None

        return ret


class JinjaExpr:
    def __init__(self, hasher: FlexiHumanHash, name: str, flexi_dict: FlexiDict) -> None:
        self.hasher = hasher
        self.name = name
        self.dict = flexi_dict
        self.args: tuple[Any, ...] | None = None
        self.kwargs: dict[str, Any] | None = None

    def __call__(self, *args: Any, **kwargs: dict[str, Any]) -> str:
        if self.hasher.rndctx is None:
            self.preprocess(args, kwargs)
            return ""

        return self.get_word()

    def __str__(self) -> str:
        if self.hasher.rndctx is None:
            self.preprocess()
            return ""

        return self.get_word()

    def get_word(self) -> str:
        r = self.hasher.rndctx
        d = self.dict
        assert r is not None
        print("dict size", d.size)
        idx = r.get_max(d.size)
        print("idx", idx)
        return d.get_entry(idx)

    def preprocess(
        self,
        args: tuple[Any, ...] = tuple(),
        kwargs: dict[str, Any] = dict(),
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.hasher.call_records.append(self)
        self.dict = self.dict.preprocess(args, kwargs)
