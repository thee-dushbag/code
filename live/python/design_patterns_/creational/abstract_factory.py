# type: ignore
from abc import ABC, abstractmethod


class Exporter(ABC):
    """This class is a interface for objects with export and imports."""

    @abstractmethod
    def export(self):
        """To Export data in some form."""

    @abstractmethod
    def convert(self):
        """For converting data to some format."""


class HighVideoExporter(Exporter):
    def export(self) -> None:
        print("Exporting in High video resolution.")

    def convert(self) -> None:
        print("Converting to High video resolution.")


class MediumVideoExporter(Exporter):
    def export(self) -> None:
        print("Exporting in Medium video resolution.")

    def convert(self) -> None:
        print("Converting to Medium video resolution.")


class LowVideoExporter(Exporter):
    def export(self) -> None:
        print("Exporting in Low video resolution.")

    def convert(self) -> None:
        print("Converting to Low video resolution.")


class HighAudioExporter(Exporter):
    def export(self) -> None:
        print("Exporting in High Audio resolution.")

    def convert(self) -> None:
        print("Converting to High Audio resolution.")


class MediumAudioExporter(Exporter):
    def export(self) -> None:
        print("Exporting in Medium Audio resolution.")

    def convert(self) -> None:
        print("Converting to Medium Audio resolution.")


class LowAudioExporter(Exporter):
    def export(self) -> None:
        print("Exporting in Low Audio resolution.")

    def convert(self) -> None:
        print("Converting to Low Audio resolution.")


class ExporterFactory(ABC):
    """For creating video and audio exporters"""

    @abstractmethod
    def video_exporter(self) -> Exporter:
        """This returns a video exporter."""

    @abstractmethod
    def audio_exporter(self) -> Exporter:
        """This returns a audio exporter."""


class HighExpoterFactory(ExporterFactory):
    def video_exporter(self) -> Exporter:
        return HighVideoExporter()

    def audio_exporter(self) -> Exporter:
        return HighAudioExporter()


class MediumExpoterFactory(ExporterFactory):
    def video_exporter(self) -> Exporter:
        return MediumVideoExporter()

    def audio_exporter(self) -> Exporter:
        return MediumAudioExporter()


class LowExpoterFactory(ExporterFactory):
    def video_exporter(self) -> Exporter:
        return LowVideoExporter()

    def audio_exporter(self) -> Exporter:
        return LowAudioExporter()


class MusicLoversFactory(ExporterFactory):
    def video_exporter(self):
        return LowVideoExporter()

    def audio_exporter(self):
        return HighAudioExporter()


class MovieLoversFactory(ExporterFactory):
    def video_exporter(self):
        return HighVideoExporter()

    def audio_exporter(self):
        return LowAudioExporter()


def user_pr(values: dict[str, str]) -> int:
    value = ""
    while not value in values:
        for key, value in values.items():
            print(f"{key}: {value}")
        value = input("Choose Exporter: ")
    return values[value]


def convert_n_export(factory: ExporterFactory) -> None:
    video_exporter: Exporter = factory.video_exporter()
    audio_exporter: Exporter = factory.audio_exporter()
    video_exporter.convert()
    video_exporter.export()
    audio_exporter.convert()
    audio_exporter.export()


class ExporterAbstractFactory:
    __factories = {}

    @staticmethod
    def register(key: str, factory: ExporterFactory) -> None:
        ExporterAbstractFactory.__factories[key] = factory

    @staticmethod
    def get_factory(key: str) -> ExporterFactory:
        if factory := ExporterAbstractFactory.__factories.get(key):
            return factory()
        else:
            raise Exception("Factory key not mapped.")


ExporterAbstractFactory.register(1, HighExpoterFactory)
ExporterAbstractFactory.register(2, LowExpoterFactory)
ExporterAbstractFactory.register(3, MediumExpoterFactory)
ExporterAbstractFactory.register(4, MusicLoversFactory)
ExporterAbstractFactory.register(5, MovieLoversFactory)

factory = ExporterAbstractFactory.get_factory(5)
v_ex: Exporter = factory.video_exporter()
a_ex: Exporter = factory.audio_exporter()
v_ex.convert()
v_ex.export()
a_ex.convert()
a_ex.export()
