import os
from pathlib import Path
from typing import Optional

SECRETS_DIR = Path(os.getenv("DOCKER_SECRETS_DIR", "/run/secrets"))

def _read_secret_file(name: str) -> Optional[str]:
    """
    Reads a Docker Secret from /run/secrets/<name>.
    Strips trailing newline that Docker injects.
    Returns None if not found.
    """
    try:
        p = SECRETS_DIR / name
        if p.exists():
            return p.read_text(encoding="utf-8").strip()
    except Exception:
        pass
    return None

def _get(var: str, secret_name: Optional[str] = None, default: Optional[str] = None) -> Optional[str]:
    """
    Resolution order:
      1. VAR_FILE env (explicit file path, works in Compose/K8s)
      2. Plain VAR env (easy in dev)
      3. Secret file (/run/secrets/<secret_name or var.lower()>)
      4. Default
    """
    # 1) explicit file path override
    file_path = os.getenv(f"{var}_FILE")
    if file_path and Path(file_path).exists():
        return Path(file_path).read_text(encoding="utf-8").strip()

    # 2) plain env var
    val = os.getenv(var)
    if val is not None:
        return val

    # 3) docker secret file
    secret = _read_secret_file(secret_name or var.lower())
    if secret is not None:
        return secret

    # 4) fallback default
    return default

class Config:
    FOOTBALL_API_URL: str = "https://v3.football.api-sports.io/"
    ODDS_API_URL: str = "https://api.the-odds-api.com/v4"

    FOOTBALL_API_KEY: str = _get("FOOTABLL_API_KEY", secret_name="football_api_key", default="NOT_SET")
    ODDS_API_KEY: str = _get("ODDS_API_KEY", secret_name="odds_api_key", default="NOT_SET")

    BETFAIR_API_KEY = _get("BETFAIR_API_KEY", secret_name="betfair_api_key", default=None)
    BETFAIR_USERNAME = _get("BETFAIR_USERNAME", secret_name="betfair_username",  default=None)
    BETFAIR_PASSWORD = _get("BETFAIR_PASSWORD", secret_name="betfair_password", default=None)

    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    MONGO_URL = f"mongodb://{MONGO_HOST}:27017/"

    BETFAIR_DATA_DIR = os.environ.get("BETFAIR_CERT_DIR", "/home/ubuntu/betfair-cert/")

    DAY_LIMIT = 2
