import dataclasses as dt
import typing as ty
import enum


class Color(enum.IntEnum):
    DARK_BLACK = enum.auto(0)
    LIGHT_BLACK = enum.auto()
    DARK_RED = enum.auto()
    LIGHT_RED = enum.auto()
    DARK_GREEN = enum.auto()
    LIGHT_GREEN = enum.auto()
    DARK_YELLOW = enum.auto()
    LIGHT_YELLOW = enum.auto()
    DARK_BLUE = enum.auto()
    LIGHT_BLUE = enum.auto()
    DARK_PURPLE = enum.auto()
    LIGHT_PURPLE = enum.auto()
    DARK_TEAL = enum.auto()
    LIGHT_TEAL = enum.auto()
    DARK_WHITE = enum.auto()
    LIGHT_WHITE = enum.auto()


def color_string(color: Color) -> str:
    match color:
        case Color.LIGHT_BLACK:
            return "\033[100m \033[0m"
        case Color.LIGHT_RED:
            return "\033[101m \033[0m"
        case Color.LIGHT_GREEN:
            return "\033[102m \033[0m"
        case Color.LIGHT_YELLOW:
            return "\033[103m \033[0m"
        case Color.LIGHT_BLUE:
            return "\033[104m \033[0m"
        case Color.LIGHT_PURPLE:
            return "\033[105m \033[0m"
        case Color.LIGHT_TEAL:
            return "\033[106m \033[0m"
        case Color.LIGHT_WHITE:
            return "\033[107m \033[0m"
        case Color.DARK_BLACK:
            return "\033[40m \033[0m"
        case Color.DARK_RED:
            return "\033[41m \033[0m"
        case Color.DARK_GREEN:
            return "\033[42m \033[0m"
        case Color.DARK_YELLOW:
            return "\033[43m \033[0m"
        case Color.DARK_BLUE:
            return "\033[44m \033[0m"
        case Color.DARK_PURPLE:
            return "\033[45m \033[0m"
        case Color.DARK_TEAL:
            return "\033[46m \033[0m"
        case Color.DARK_WHITE:
            return "\033[47m \033[0m"


def hex_color(color: Color) -> str:
    if color < 10: return str(int(color))
    return chr(ord("A") + color - 10)


@dt.dataclass(slots=True)
class Rect:
    x: float
    y: float
    width: float
    height: float
    color: Color
    children: list["Rect"] = dt.field(default_factory=list, repr=False)

    def flatten(self) -> ty.Iterable["Rect"]:
        while self.children:
            child = self.children.pop(0)
            child.x = self.x + child.x / 100 * self.width
            child.y = self.y + child.y / 100 * self.height
            child.width = child.width / 100 * self.width
            child.height = child.height / 100 * self.height
            yield child
            yield from child.flatten()

    def flatten_self(self) -> ty.Iterable["Rect"]:
        yield self
        yield from self.flatten()


@dt.dataclass(slots=True)
class Image:
    width: int
    height: int
    bg: Color = Color.DARK_BLACK

    def create_canvas(self) -> list[list[Color]]:
        canvas: list[list[Color]] = []
        for _ in range(self.height):
            row: list[Color] = [self.bg] * self.width
            canvas.append(row)
        return canvas

    def compile_canvas(
        self,
        canvas: list[list[Color]],
        str_color: ty.Callable[[Color], str] = color_string,
    ) -> str:
        return "\n".join("".join(map(str_color, row)) for row in canvas)

    def draw(
        self,
        image: Rect | None = None,
        canvas: list[list[Color]] | None = None,
        str_color: ty.Callable[[Color], str] = color_string,
    ) -> str:
        canvas = self.create_canvas() if canvas is None else canvas
        if image is None:
            return self.compile_canvas(canvas, str_color)
        for rect in image.flatten_self():
            row_start = round(rect.y / 100 * self.height)
            row_span = round(rect.height / 100 * self.height)
            column_start = round(rect.x / 100 * self.width)
            column_span = round(rect.width / 100 * self.width)

            for row in range(row_start, row_start + row_span):
                for column in range(column_start, column_start + column_span):
                    try:
                        canvas[row][column] = rect.color
                    except IndexError:
                        ...
        return self.compile_canvas(canvas, str_color)



face = Rect(
    10,
    10,
    80,
    80,
    Color.DARK_YELLOW,
    [
        Rect(
            11,
            11,
            78,
            78,
            Color.DARK_YELLOW,
            [
                Rect(
                    0,
                    0,
                    100,
                    45,
                    Color.DARK_YELLOW,
                    [
                        Rect(
                            3,
                            3,
                            42,
                            90,
                            Color.LIGHT_WHITE,
                            [
                                Rect(
                                    15,
                                    15,
                                    70,
                                    70,
                                    Color.DARK_BLACK,
                                    [Rect(75, 0, 25, 25, Color.LIGHT_WHITE)],
                                )
                            ],
                        ),
                        Rect(
                            54,
                            3,
                            42,
                            90,
                            Color.LIGHT_WHITE,
                            [
                                Rect(
                                    15,
                                    15,
                                    70,
                                    70,
                                    Color.DARK_BLACK,
                                    [Rect(75, 0, 25, 25, Color.LIGHT_WHITE)],
                                )
                            ],
                        ),
                    ],
                ),
                Rect(
                    0,
                    45,
                    100,
                    55,
                    Color.LIGHT_BLACK,
                    [Rect(20, 30, 60, 40, Color.DARK_BLACK)],
                ),
            ],
        )
    ],
)

flag = Rect(
    0,
    0,
    100,
    100,
    Color.DARK_WHITE,
    [
        Rect(0, 0, 100, 10, Color.DARK_RED),
        Rect(0, 20, 100, 10, Color.DARK_RED),
        Rect(0, 40, 100, 10, Color.DARK_RED),
        Rect(0, 60, 100, 10, Color.DARK_RED),
        Rect(0, 80, 100, 10, Color.DARK_RED),
        Rect(
            0,
            0,
            50,
            50,
            Color.DARK_BLUE,
            [
                Rect(
                    0,
                    0,
                    100,
                    10,
                    Color.DARK_BLUE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_WHITE),
                        Rect(20, 0, 10, 100, Color.DARK_WHITE),
                        Rect(40, 0, 10, 100, Color.DARK_WHITE),
                        Rect(60, 0, 10, 100, Color.DARK_WHITE),
                        Rect(80, 0, 10, 100, Color.DARK_WHITE),
                    ],
                ),
                Rect(
                    0,
                    10,
                    100,
                    10,
                    Color.DARK_WHITE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_BLUE),
                        Rect(20, 0, 10, 100, Color.DARK_BLUE),
                        Rect(40, 0, 10, 100, Color.DARK_BLUE),
                        Rect(60, 0, 10, 100, Color.DARK_BLUE),
                        Rect(80, 0, 10, 100, Color.DARK_BLUE),
                    ],
                ),
                Rect(
                    0,
                    20,
                    100,
                    10,
                    Color.DARK_BLUE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_WHITE),
                        Rect(20, 0, 10, 100, Color.DARK_WHITE),
                        Rect(40, 0, 10, 100, Color.DARK_WHITE),
                        Rect(60, 0, 10, 100, Color.DARK_WHITE),
                        Rect(80, 0, 10, 100, Color.DARK_WHITE),
                    ],
                ),
                Rect(
                    0,
                    30,
                    100,
                    10,
                    Color.DARK_WHITE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_BLUE),
                        Rect(20, 0, 10, 100, Color.DARK_BLUE),
                        Rect(40, 0, 10, 100, Color.DARK_BLUE),
                        Rect(60, 0, 10, 100, Color.DARK_BLUE),
                        Rect(80, 0, 10, 100, Color.DARK_BLUE),
                    ],
                ),
                Rect(
                    0,
                    40,
                    100,
                    10,
                    Color.DARK_BLUE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_WHITE),
                        Rect(20, 0, 10, 100, Color.DARK_WHITE),
                        Rect(40, 0, 10, 100, Color.DARK_WHITE),
                        Rect(60, 0, 10, 100, Color.DARK_WHITE),
                        Rect(80, 0, 10, 100, Color.DARK_WHITE),
                    ],
                ),
                Rect(
                    0,
                    50,
                    100,
                    10,
                    Color.DARK_WHITE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_BLUE),
                        Rect(20, 0, 10, 100, Color.DARK_BLUE),
                        Rect(40, 0, 10, 100, Color.DARK_BLUE),
                        Rect(60, 0, 10, 100, Color.DARK_BLUE),
                        Rect(80, 0, 10, 100, Color.DARK_BLUE),
                    ],
                ),
                Rect(
                    0,
                    60,
                    100,
                    10,
                    Color.DARK_BLUE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_WHITE),
                        Rect(20, 0, 10, 100, Color.DARK_WHITE),
                        Rect(40, 0, 10, 100, Color.DARK_WHITE),
                        Rect(60, 0, 10, 100, Color.DARK_WHITE),
                        Rect(80, 0, 10, 100, Color.DARK_WHITE),
                    ],
                ),
                Rect(
                    0,
                    70,
                    100,
                    10,
                    Color.DARK_WHITE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_BLUE),
                        Rect(20, 0, 10, 100, Color.DARK_BLUE),
                        Rect(40, 0, 10, 100, Color.DARK_BLUE),
                        Rect(60, 0, 10, 100, Color.DARK_BLUE),
                        Rect(80, 0, 10, 100, Color.DARK_BLUE),
                    ],
                ),
                Rect(
                    0,
                    80,
                    100,
                    10,
                    Color.DARK_BLUE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_WHITE),
                        Rect(20, 0, 10, 100, Color.DARK_WHITE),
                        Rect(40, 0, 10, 100, Color.DARK_WHITE),
                        Rect(60, 0, 10, 100, Color.DARK_WHITE),
                        Rect(80, 0, 10, 100, Color.DARK_WHITE),
                    ],
                ),
                Rect(
                    0,
                    90,
                    100,
                    10,
                    Color.DARK_WHITE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_BLUE),
                        Rect(20, 0, 10, 100, Color.DARK_BLUE),
                        Rect(40, 0, 10, 100, Color.DARK_BLUE),
                        Rect(60, 0, 10, 100, Color.DARK_BLUE),
                        Rect(80, 0, 10, 100, Color.DARK_BLUE),
                    ],
                ),
                Rect(
                    0,
                    100,
                    100,
                    10,
                    Color.DARK_BLUE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_WHITE),
                        Rect(20, 0, 10, 100, Color.DARK_WHITE),
                        Rect(40, 0, 10, 100, Color.DARK_WHITE),
                        Rect(60, 0, 10, 100, Color.DARK_WHITE),
                        Rect(80, 0, 10, 100, Color.DARK_WHITE),
                    ],
                ),
                Rect(
                    0,
                    50,
                    100,
                    10,
                    Color.DARK_WHITE,
                    [
                        Rect(0, 0, 10, 100, Color.DARK_BLUE),
                        Rect(20, 0, 10, 100, Color.DARK_BLUE),
                        Rect(40, 0, 10, 100, Color.DARK_BLUE),
                        Rect(60, 0, 10, 100, Color.DARK_BLUE),
                        Rect(80, 0, 10, 100, Color.DARK_BLUE),
                    ],
                ),
            ],
        ),
    ],
)

image = Image(148, 60, Color.LIGHT_TEAL)
image = Image(80, 20, Color.LIGHT_PURPLE)

print(image.draw())
print()
print(image.draw(face))
print()
print(image.draw(flag))
