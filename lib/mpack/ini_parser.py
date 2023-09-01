import re
from typing import Any
from typing_extensions import Self

class IniParser:
    def __init__(
        self: Self,
        dlm: str = "=",
        tkdlm: str = "\n",
        btk: str = "[",
        etk: str = "]",
        dhd: str = "DEFAULT",
    ) -> None:
        self.dlm = dlm
        self.tkdlm = tkdlm
        self.beg_el = btk
        self.end_el = etk
        self.head_pat = re.compile(f"\{btk}(.+)\{etk}")  # type: ignore
        self.val_pat = re.compile(f"(.+)\{dlm}(.*)")  # type: ignore
        self.dhd = dhd

    def _add_val(
        self,
        data: dict[str, dict[str, str]],
        head: str,
        key: str | None = None,
        value: str | None = None,
    ) -> dict[str, dict[str, str]]:
        if head not in data:
            data[head] = {}
        if not key:
            return data
        data[head][key] = value or ""  # type: ignore
        return data

    def parse(self: Self, text: str) -> dict[str, dict[str, str]]:
        data: dict[str, dict[str, str]] = {}
        tokens: list[str] = text.split(self.tkdlm)
        cur_hd = self.dhd
        for token in tokens:
            if not token:
                continue
            if _f := self.head_pat.findall(token):
                cur_hd = _f[0].strip()
                self._add_val(data, cur_hd)
            elif _f := self.val_pat.findall(token):
                self._add_val(data, cur_hd, _f[0][0].strip(), _f[0][1].strip())
            else:
                raise Exception(f"Identification token at: '{token}'")
        return data

    def serialize(self: Self, data: dict[Any, dict[Any, Any]]) -> str:
        serialized: str = ""
        for head, maps in data.items():
            head = str(head).strip()
            if not head:
                raise Exception(f"Invalid head: \"'{head}'\"")
            lines: list[str] = [f"{self.beg_el}{head}{self.end_el}"]
            for key, val in maps.items():
                key, val = str(key).strip(), str(val).strip()
                if not key:
                    raise Exception(f"Invalid key at: \"'{key}'{self.dlm}'{val}'\"")
                lines.append(f"{key}{self.dlm}{val}")
            serialized += self.tkdlm.join(lines) + self.tkdlm
        return serialized

