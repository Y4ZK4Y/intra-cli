from intra_cli.config import Config
from typing import Optional
import requests

def get_access_token() -> Optional[str]:
    config = get_config()
    if not config.is_configured():
        raise ValueError("Client ID and secret got fucked")
    
    try:
        response = requests.post(
            f"{config.api_base_url}/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": config.client_id,
                "client_secret": config.client_secret
            },
            timeout=15
        )
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")

        if access_token:
            # save
            config.access_token = access_token
            return access_token
        else:
            return None
        
    except requests.exceptions.requestExceptiopn as e:
        raise Exception(f"{e}")


def is_token_good() -> str:
    config = get_config()
    if config.has_token():
        return config.access_token
    else
        return get_access_token()
