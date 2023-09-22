from unittest import TestCase, mock

from bigchain import BigChain
from mpack.number_reader.locales import english_locale as locale
from mpack.number_reader.reader import NumberReader

reader = NumberReader(locale)


def stepper(chain: BigChain, *steps: str):
    for step in steps:
        chain = getattr(chain, step)()
    return chain


def from_number(*steps: int):
    return [reader.read(i) for i in steps]


class ChainTest(TestCase):
    sep = " | -> | "
    big = BigChain(sep)

    def test_step_one_and_two(self):
        str_steps = from_number(1, 2)
        result = self.sep.join(str_steps)
        bresult = self.big.one().two().str_steps
        self._print_result(str_steps, result, bresult)
        self.assertEqual(result, bresult, f"{result!r} != {bresult!r}")

    def test_walk_step_function(self):
        steps = (*range(1, 11),)
        str_steps = from_number(*steps)
        result = self.sep.join(str_steps)
        bresult = stepper(self.big, *str_steps).str_steps
        self._print_result(str_steps, result, bresult)
        self.assertEqual(result, bresult, f"{result!r} != {bresult!r}")

    def _print_result(self, str_steps, result, bresult):
        print(f"Found:\n\t{str_steps=}\n\t{result=}\n\t{bresult=}\n")

    @mock.patch("test_orm.ChainTest.big")
    def test_step_three_and_four(self, mbig: mock.MagicMock):
        steps = (*range(1, 11),)
        str_steps = from_number(*steps)
        mbig.one.return_value.two.return_value.three.return_value.four.return_value.five.return_value.six.return_value.seven.return_value.eight.return_value.nine.return_value.ten.return_value.str_steps = (
            result := self.sep.join(str_steps)
        )
        bresult = stepper(mbig, *str_steps).str_steps
        self._print_result(str_steps, result, bresult)
        self.assertEqual(result, bresult, f"{result!r} != {bresult!r}")
