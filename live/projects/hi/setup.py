from pathlib import Path

import hi.__meta__ as meta
import setuptools

WORKING_DIR = Path(__file__).parent
README = WORKING_DIR / "README.md"
long_description = README.read_text()

setuptools.setup(
    name='hi',
    version=meta.__version__,
    description='Commonly used hi and say_hi functions.',
    long_description=long_description,
    author=meta.__author__,
    author_email=meta.__author_email__,
    packages=['hi'],
    requires=['click', 'rich'],
    maintainer=meta.__maintainer__,
    maintainer_email=meta.__maintainer_email__,
    keywords=['say_hi', 'hi', 'hello', 'hi python'],
)
