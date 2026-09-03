import httpx
import typer
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table


app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """Scrape simple data from web pages."""


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url


@app.command()
def titles(urls: list[str] = typer.Argument(..., help="URLs to scrape.")) -> None:
    table = Table(title="Page Titles")
    table.add_column("URL")
    table.add_column("Title")
    table.add_column("Status")

    for url in urls:
        normalized_url = normalize_url(url)
        try:
            response = httpx.get(normalized_url, follow_redirects=True, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("title")
            table.add_row(normalized_url, title.get_text(strip=True) if title else "", str(response.status_code))
        except httpx.HTTPError as error:
            table.add_row(normalized_url, str(error)[:80], "ERROR")

    console.print(table)
