from __future__ import annotations
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Any

registry: dict[str, FlexiDict] = {}

class FlexiDict(ABC):
    @abstractmethod
    def get_entry(self, n: int) -> str: ...

    @property
    @abstractmethod
    def size(self) -> int: ...

    @staticmethod
    def register(name: str, d: FlexiDict) -> None:
        registry[name] = d

    @staticmethod
    def get_registry() -> dict[str, FlexiDict]:
        return registry

T = TypeVar("T", bound=type[FlexiDict])

def register_dict(name: str) -> Callable[[T], T]:
    def decorator(cls: T) -> T:
        FlexiDict.register(name, cls())
        return cls

    return decorator

class FlexiTextDict(FlexiDict):
    def __init__(self, name: str, words: list[str], min: int = 0, max: int = 2048) -> None:
        if min != 0 or max != 2048:
            self.words = [w for w in words if len(w) > min and len(w) < max]
        else:
            self.words = words
        self.sz = len(words)

    def get_entry(self, n: int) -> str:
        return self.words[n]

    @property
    def size(self) -> int:
        return self.sz

    @staticmethod
    def from_file(name: str, path: str) -> FlexiTextDict:
        fullpath = Path(path).resolve()
        with open(fullpath, "r") as file:
            lines = file.read().splitlines()
        d = FlexiTextDict(name, lines)
        FlexiDict.register(name, d)
        return d

@register_dict("hex")
class FlexiHexDict(FlexiDict):
    def __init__(self, size: int = 4) -> None:
        self.sz = size

    def get_entry(self, n: int) -> str:
        return f"{n:0{self.sz}x}" 

    @property
    def size(self) -> int:
        num_bits = self.sz * 4
        ret: int = 2 ** num_bits
        return ret

@register_dict("decimal")
class FlexiDecimalDict(FlexiDict):
    def __init__(self, size: int = 4) -> None:
        self.sz = size

    def get_entry(self, n: int) -> str:
        return f"{n:0{self.sz}d}" 

    @property
    def size(self) -> int:
        ret: int = 10 ** self.sz
        return ret

FlexiTextDict.from_file("noun", "data/build/noun")
FlexiTextDict.from_file("adj", "data/build/adjective")
FlexiTextDict.from_file("verb", "data/build/verb")
FlexiTextDict.from_file("city", "data/build/city")
FlexiTextDict.from_file("first-name", "data/build/first-name")
FlexiTextDict.from_file("last-name", "data/build/last-name")
FlexiTextDict.from_file("female-name", "data/build/female-name")
FlexiTextDict.from_file("male-name", "data/build/male-name")
