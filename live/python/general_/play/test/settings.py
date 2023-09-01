from utils import Config
from pathlib import Path
from model import CONFIG_KEY as model_CONFIG_KEY
from views import CONFIG_KEY as views_CONFIG_KEY

# APPLICATION CONSTANTS
PROJECT_DIR = Path(__file__).parent.absolute()
SQLITE3_FILENAME = 'notes-site.sqlite3'
TEMPLATES_DIR = PROJECT_DIR / 'templates'
STATIC_DIR = PROJECT_DIR / 'static'
DB_DNS = f'sqlite:/{PROJECT_DIR}/{SQLITE3_FILENAME}'

# APPLICATION SETTINGS
model_config = Config(
    model_CONFIG_KEY,
    dns=DB_DNS,
    filename=SQLITE3_FILENAME,
    db_pack=None
)
views_config = Config(
    views_CONFIG_KEY,
    staticdir=str(STATIC_DIR),
    templatedir=str(TEMPLATES_DIR)
)

config_registry: list[Config] = [
    views_config,
    model_config
]