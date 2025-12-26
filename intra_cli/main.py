# entry point - 

import os
from pathlib import Path

import typer
import requests
from dotenv import load_dotenv

app = typer.Typer()


load_dotenv(Path(".env")) # reads variables froma .env file and sets them in os.environ

def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise typer.Exit(f"missing env var {name}")
    return value

@app.callback()
def main():
    pass


@app.command()
def ping():
    client_id = get_env("INTRA_CLIENT_UID")
    client_secret = get_env("INTRA_CLIENT_SECRET")
    api_base = get_env("INTA_API_BASE_URL")
    api_v2_base = get_env("V2_BASE")

    token_res = requests.post(
        f"{api_base}/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        },
        timeout=15,
    )

    token_res.raise_for_status()
    access_token = token_res.json()["access_token"]

    r = requests.get(
        f"{api_v2_base}/campus",
        params={"per_page": 1},
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    r.raise_for_status()
    campuses = r.json()

    first_name = campuses[0].get("name") if campuses else "unknown"
    print(f"OK ✅ Connected. First campus: {first_name}")

    

if __name__ == "__main__":
    app()
