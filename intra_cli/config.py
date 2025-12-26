# credentials: loads credentials from .env
# tokens: saves/loads tokens from a config file

import os
from pathlib import Path
from dotenv import load_dotenv
import json
from typing import Optional

class Config:
    def __init__(self):
        load_dotenv(Path(".env"))

        self.config_dir = Path.home() / ".config" / "intra-cli"
        self.config_file = self.config_dir / "config.json"

        self.config_dir.mkdir(parents=True, exist_ok=True) 

        self._config = self._load_config()


    def _load_config(self) -> dict:
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=2)

    @property
    def client_id(self) -> Optional[str]:
        return os.getenv("INTRA_CLIENT_UID")

    @property
    def client_secret(self) -> Optional[str]:
        return os.getenv("INTRA_CLIENT_SECRET")

    @property
    def api_base_url(self) -> Optional[str]:
        return os.getenv("INTRA_API_BASE_URL")

    @property
    def access_token(self) -> Optional[str]:
        return self._config.get("access_token")

    @access_token.setter
    def access_token(self, value: str):
        self._config["access_token"] = value
        self._save_config()

    def is_configured(self) -> bool:
        return self.client_id is not None and self.client_secret is not None

    def has_token(self) -> bool:
        return self.access_token is not None

_config_instance = None

def get_config() -> Config:
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
