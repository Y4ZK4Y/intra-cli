# entry point - 

import typer
from intra_cli.api_client import ApiClient
from intra_cli.config import get_config
from intra_cli.auth import get_access_token

app = typer.Typer()

@app.command(name="ping")
def ping():
    """Test connection to 42 API"""
    try:
        client = ApiClient()
        campuses = client.get_campus(per_page=1)
        
        first_name = campuses[0].get("name") if campuses else "unknown"
        typer.echo("OK - Connected.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command(name="login")
def login():
    """Get a new access token"""
    try:
        token = get_access_token()
        if token:
            typer.echo("Successfully authenticated!")
        else:
            typer.echo("Failed to get token", err=True)
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

def main():
    app()

if __name__ == "__main__":
    app()
