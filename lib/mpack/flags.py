def flag_on(value: int, flag: int) -> int:
    return value | flag


def flag_off(value: int, flag: int) -> int:
    return (value ^ flag) if flag_enabled(value, flag) else value


def flag_enabled(value: int, flag: int) -> bool:
    return (value & flag) == flag


def flag_disabled(value: int, flag: int) -> bool:
    return not flag_enabled(value, flag)
