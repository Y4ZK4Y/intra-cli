# make authenticated API calls - wrapper around HTTP requests to 42 api

from typing import Optional, Dict, Any
import requests
from intra_cli.config import get_config
from intra_cli.auth import is_token_good

class ApiClient:
    def __init__(self):
        self.config = get_config()
        self.api_base = self.config.api_base_url

    def _get_headers(self) -> Dict[str, str]:
        """
        get headers for authentication token
        """
        token = is_token_good()
        if not token:
            raise ValueError("No access token available")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Docstring for get
        
        :param self: Description
        :param endpoint: Description
        :type endpoint: str
        :param params: Description
        :type params: Optional[Dict]
        :return: Description
        :rtype: Dict[str, Any]
        """
        url = f"{self.api_base}{endpoint}"
        headers = self._get_headers()

        response = requests.get(
            url, headers=headers, params=params, timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_campus(self, per_page: int = 1) -> Dict[str, Any]:
        return self.get("/v2/campus", params={"per_page": per_page})
    

    def get_me(self) -> Dict[str, Any]:
        return self.get("/v2/me")


