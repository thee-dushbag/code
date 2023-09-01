from itertools import chain
from typing import Any, Callable, Sequence, Type, Union


class perfect_dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type_maps_: dict[str, Callable[[Any, Any], Any]] = {
            list.__name__: self._update_list_value,
            tuple.__name__: self._update_tuple_value,
            str.__name__: self._update_string_value,
            dict.__name__: self._update_dict_value,
            int.__name__: self._update_int_value,
        }

    def add_type_map(self, typename: Type[Any], updater: Callable[[Any, Any], Any]):
        self._type_maps_[typename.__name__] = updater

    def perfect_update(self, other: Union[dict, "perfect_dict"]):
        for ikey in set(self.keys()).intersection(set(other.keys())):
            self[ikey] = self._update_values(self[ikey], other[ikey])

    def _update_string_value(self, current_value: str, other_value: str):
        return other_value

    def _update_int_value(self, current_value: str, other_value: str):
        return other_value

    def _update_seq_value(self, stype: Type, current_value: Sequence[Any], other_value: Sequence[Any]):
        store, hashes = [], set()
        def _mhash_impl(arg):
            arg = perfect_dict(**arg) if type(arg) == dict else arg
            if type(arg) == perfect_dict:
                return arg._mhash()
            return str(hash(arg))
        def mhash(arg):
            hash_v = _mhash_impl(arg)
            if hash_v not in hashes:
                hashes.add(hash_v)
                store.append(arg)
            return hash_v
        for val in chain(current_value, other_value):
            mhash(val)
        return stype(store)

    def _update_list_value(self, current_value: list[Any], other_value: list[Any]):
        return self._update_seq_value(list, current_value, other_value)

    def _update_tuple_value(self, current_value: tuple[Any, ...], other_value: tuple[Any, ...]):
        return self._update_seq_value(tuple, current_value, other_value)

    def _mhash(self):
        return ",".join(f"{key!s}={value!s}" for key, value in self.items())

    def _update_dict_value(self, current_value: dict, other_value: dict):
        pcval = perfect_dict(**current_value)
        pcval.perfect_update(other_value)
        return pcval

    def _type_maps(self, _type: Type):
        assert (
            _type.__name__ in self._type_maps_
        ), f"Type[{_type.__name__}] update is unknown"
        return self._type_maps_[_type.__name__]

    def _update_value_type(self, value_type: Type, current_value: Any, other_value: Any):
        updater = self._type_maps(value_type)
        return updater(current_value, other_value)

    def _update_values(self, current_value: Any, other_value: Any):
        if type(other_value) == (t := type(current_value)):
            return self._update_value_type(t, current_value, other_value)
        return current_value
