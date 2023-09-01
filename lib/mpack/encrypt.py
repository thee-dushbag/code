import copy  # deepcopy
import typing  # Any
import random  # shuffle

__all__ = ["Encrypter"]


class Encrypter:
    def __init__(self, maps: dict|None = None, charlen: int = 255) -> None:
        if maps:
            self.set_mappings(maps)
            return
        mappings = self.get_random_mappings([chr(i) for i in range(charlen)])
        self.__encrypt_maps = str.maketrans(mappings)
        self.__decrypt_maps = str.maketrans(self.flip_dict_kv(self.__encrypt_maps))

    def get_mappings(self) -> dict[dict[int, str], dict[int, str]]:
        return dict(encrypt_map=self.__encrypt_maps, decrypt_map=self.__decrypt_maps) # type: ignore

    def set_mappings(self, mappings: dict[dict[int, str], dict[int, str]]) -> None:
        self.__decrypt_maps = mappings["decrypt_map"] # type: ignore
        self.__encrypt_maps = mappings["encrypt_map"] # type: ignore

    def encrypt(self, string: str) -> str:
        return string.translate(self.__encrypt_maps)

    @staticmethod
    def flip_dict_kv(
        mapping: dict[typing.Any, typing.Any]
    ) -> dict[typing.Any, typing.Any]:
        return {value: key for key, value in mapping.items()}

    @staticmethod
    def get_random_mappings(values: list[typing.Any]) -> dict[typing.Any : typing.Any]: # type: ignore
        mappings = copy.deepcopy(values)
        random.shuffle(mappings)
        return {value: mapping for value, mapping in zip(values, mappings)}

    def decrypt(self, string: str) -> str:
        return string.translate(self.__decrypt_maps)

    @staticmethod
    def from_json(
        maps: dict[str, dict], ekey: str = "encrypt_map", dkey: str = "decrypt_map"
    ) -> "Encrypter":
        mapping = {}
        emap = {int(key): value for key, value in maps[ekey].items()}
        dmap = {int(key): value for key, value in maps[dkey].items()}
        mapping["encrypt_map"] = emap
        mapping["decrypt_map"] = dmap
        return Encrypter(maps=mapping)
