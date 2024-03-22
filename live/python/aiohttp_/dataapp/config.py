from pathlib import Path
import typing as ty

WORKING_DIR = Path(__file__).parent
USERSDATA_FILE = WORKING_DIR / 'usersdata.yaml'
PersistTypes = ty.Literal['yaml', 'json']
PERSIST_TYPE: PersistTypes = 'yaml'