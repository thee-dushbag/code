from pathlib import Path
import typing as ty

WORKING_DIR = Path(__file__).parent
USERSDATA_FILE = WORKING_DIR / 'usersdata.yaml'
PERSIST_TYPE: ty.Literal['yaml', 'json'] = 'yaml'