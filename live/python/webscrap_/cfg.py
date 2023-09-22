from os import getenv

from yarl import URL

# USERNAME = getenv("STORE_USERNAME")
# PASSWORD = getenv("STORE_PASSWORD")
HOST, PORT = "localhost", 5052
BASE_URL = URL(f"http://{HOST}:{PORT}")
STORE_URL = BASE_URL.with_path("user_data_store")
ADDUSER_URL = BASE_URL.with_path("add_user")
RMUSER_URL = BASE_URL.with_path("rm_user")

# if not USERNAME and not PASSWORD:
#     print(f"Invalid AUTH: {USERNAME} {PASSWORD}")
#     exit(-1)
