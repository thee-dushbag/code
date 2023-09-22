# type: ignore
import copy
import json
import os
from abc import ABC, abstractmethod
from typing import Any


class DataSource(ABC):
    @abstractmethod
    def read(self: "DataSource", pmt: str = "") -> str:
        """Returns the data read from the source."""

    @abstractmethod
    def write(self: "DataSource", data: str) -> None:
        """Writes data into the data source."""


class Formatter(ABC):
    @abstractmethod
    def format(self: "Formatter", data: dict[str : dict[str, str]]) -> str:
        """Converts the data to some given formart."""

    @abstractmethod
    def loader(self: "Formatter", data: str) -> dict[str : dict[str:str]]:
        """Converts formatted data back to its original."""


class CollectData(ABC):
    @abstractmethod
    def collect(self, formatter: Formatter, source: DataSource) -> None:
        """For collecting data and writing it to the
        datasource and reading from the datasource."""


class StdOutDataSource(DataSource):
    def read(self: "DataSource", pmt: str = "Reader:>") -> str:
        return input(pmt.title() + " ")

    def write(self: "DataSource", data: str) -> None:
        print(f"Writer:\n{data}")


class IniFormatter(Formatter):
    def __init__(self: "IniFormatter", dlm: str = "="):
        self.dlm = dlm

    def format(self: "Formatter", data: dict[str : dict[str:str]]) -> str:
        formatted: str = ""
        for section in data:
            formatted += "[" + section + "]\n"
            for key, value in data[section].items():
                formatted += key + self.dlm + value + "\n"
        return formatted

    def loader(self: "Formatter", data: str) -> dict[str : dict[str:str]]:
        result: dict = dict(default=dict())
        current_section = result["default"]
        lines: list[str] = data.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                section_name = line[1:-1]
                result[section_name] = dict()
                current_section = result[section_name]
            elif self.dlm in line:
                key, value = line.split(self.dlm)
                current_section[key] = value
        return result


class JsonFormatter(Formatter):
    def format(self: "Formatter", data: dict[str : dict[str, str]]) -> str:
        return json.dumps(data)

    def loader(self: "Formatter", data: str) -> dict[str : dict[str:str]]:
        return json.loads(data)


class UserDataCollectorIni(CollectData):
    def __init__(self, formatter: Formatter, source: DataSource, *section: str):
        self.formatter: Formatter = formatter
        self.source: DataSource = source
        self.sections: tuple[str, ...] = section

    def collect(self) -> None:
        collected: dict[str:str] = dict()
        for section in self.sections:
            collected[section] = self.get_data(
                section, ["name", "age", "email", "tell"]
            )
        formatted_data = self.formatter.format(collected)
        self.source.write(formatted_data)

    def get_data(self, section, fields: list[str]):
        result = dict()
        for field in fields:
            result[field] = self.source.read(f"{section}@{field}")
        return result


class FileDatasource(DataSource):
    def __init__(self: "FileDatasource", file: str) -> None:
        assert os.path.exists(file), f"File '{file}' not found."
        self.file = open(file, "r+")

    def read(self: "DataSource", pmt: str = "") -> str:
        return self.file.readline().strip()

    def write(self: "DataSource", data: str) -> None:
        self.file.write(data + "\n")

    def __del__(self) -> None:
        if not self.file.closed:
            self.file.close()


class IniFileDataSource(FileDatasource):
    def __init__(
        self: "IniFileDataSource", file: str, dlm: str = "=", secdlm: str = "@"
    ) -> None:
        super().__init__(file)
        self.formatter = IniFormatter()
        self.data = self.formatter.loader(self.file.read())
        self.file.close()
        self.file = open(file, "w")
        self.dlm = dlm
        self.secdlm = secdlm

    def parse(self: "IniFileDataSource", line: str) -> list[str]:
        if self.secdlm in line:
            section, data = line.split(self.secdlm)
        else:
            section = "default"
            data = line
        return [section, data]

    def read(self: "DataSource", pmt: str) -> str:
        section, data = self.parse(pmt)
        return self.data[section][data]

    def write(self: "DataSource", data: str) -> None:
        section, data = self.parse(data)
        key, value = data.split(self.dlm)
        if not section in self.data:
            self.data[section] = dict()
        self.data[section][key.strip()] = value.strip()

    def __del__(self) -> None:
        self.file.write(self.formatter.format(self.data))
        return super().__del__()


class MyMixinDataSource(IniFileDataSource, StdOutDataSource):
    def __init__(self: "IniFileDataSource", file: str) -> None:
        super().__init__(file)

    def write(self: "DataSource", data: str) -> None:
        return StdOutDataSource.write(self, data)

    def read(self: "DataSource", pmt: str = "") -> str:
        return IniFileDataSource.read(self, pmt)


if __name__ == "__main__":
    formatter = JsonFormatter()
    source = MyMixinDataSource("file.txt")
    collector = UserDataCollectorIni(
        formatter,
        source,
        "UserDataIni1",
        "UserDataIni2",
        "UserDataIni3",
        "UserDataIni4",
    )
    collector.collect()
