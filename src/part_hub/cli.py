"""Command-line interface for PartHub."""

import typer
import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from part_hub.service import PartHubService

app = typer.Typer(
    name="part-hub",
    help="Fast electronic component search and direct datasheet CDN resolver.",
    add_completion=False,
)
console = Console()
service = PartHubService()


@app.command()
def search(
    query: str = typer.Argument(..., help="Part number or keyword (e.g., STM32F405, RP2040, TPS62160)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results to display"),
):
    """Search electronic parts across distributor catalogs."""
    console.print(f"[cyan]Searching for:[/cyan] [bold]{query}[/bold]...")
    results = service.search(query, limit=limit)
    if not results:
        console.print("[red]No parts found.[/red]")
        return

    table = Table(title=f"Search Results for '{query}'")
    table.add_column("Part ID", style="bold yellow")
    table.add_column("MPN", style="bold green")
    table.add_column("Manufacturer", style="white")
    table.add_column("Package", style="cyan")
    table.add_column("Stock", style="magenta")
    table.add_column("Price (1+)", style="green")

    for p in results:
        price_str = f"${p.price_usd:.4f}" if p.price_usd is not None else "-"
        table.add_row(
            p.part_id,
            p.mpn,
            p.manufacturer or "-",
            p.package or "-",
            str(p.stock or 0),
            price_str,
        )

    console.print(table)


@app.command()
def resolve(
    part: str = typer.Argument(..., help="Part ID (e.g. C15742) or MPN (e.g. STM32F405RGT6, TPS62160)"),
):
    """Resolve direct un-gated PDF link on CDN (0 bytes stored locally)."""
    console.print(f"[cyan]Resolving datasheet for:[/cyan] [bold]{part}[/bold]...")
    info = service.resolve_datasheet_url(part)
    if not info:
        console.print(f"[red]Could not resolve datasheet for {part}.[/red]")
        return

    size_mb = f"{info.content_length_bytes / (1024 * 1024):.2f} MB" if info.content_length_bytes else "Unknown"
    panel = Panel(
        f"[bold green]Direct CDN URL:[/bold green]\n{info.direct_cdn_url}\n\n"
        f"[yellow]MPN:[/yellow] {info.mpn} | [yellow]Part ID:[/yellow] {info.part_id} | [yellow]Size:[/yellow] {size_mb}",
        title="✓ Datasheet Resolved",
        border_style="green",
    )
    console.print(panel)


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Bind host"),
    port: int = typer.Option(8000, "--port", "-p", help="Bind port"),
):
    """Start the FastAPI backend server for your frontend UI."""
    console.print(f"[bold green]Starting PartHub API on http://{host}:{port}[/bold green]")
    console.print(f"[cyan]Interactive Swagger documentation at: http://{host}:{port}/docs[/cyan]")
    uvicorn.run("part_hub.api:app", host=host, port=port, reload=True)


def main():
    app()


if __name__ == "__main__":
    main()
