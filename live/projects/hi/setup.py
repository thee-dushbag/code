import setuptools, yaml
import hi.__meta__ as meta
from pathlib import Path

WORKING_DIR = Path(__file__).parent
CONFIG = WORKING_DIR / 'config.yml'
README = WORKING_DIR / 'README.md'

with CONFIG.open() as file:
    config = yaml.safe_load(file)
long_description = README.read_text()

setuptools.setup(
    name=config['package_name'],
    version=meta.__version__,
    description=config.get('description', ''),
    long_description=long_description,
    author=meta.__author__,
    author_email=meta.__author_email__,
    packages=config['packages'],
    requires=config.get('requirements', []),
    maintainer=meta.__maintainer__,
    maintainer_email=meta.__maintainer_email__,
    keywords=config.get('keywords', []),
)