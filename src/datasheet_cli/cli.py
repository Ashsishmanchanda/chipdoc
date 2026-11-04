"""Command-line interface for datasheet-cli."""

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="datasheet-cli",
    help="Extract reference designs from component datasheets and synthesize KiCad schematics.",
    add_completion=False,
)
console = Console()


@app.command()
def fetch(
    mpn: str = typer.Argument(..., help="Manufacturer Part Number (e.g., TPS54302, STM32F405)"),
    output_dir: str = typer.Option("./downloads", "--out", "-o", help="Directory to save downloaded datasheets"),
):
    """Fetch datasheet and package metadata for a part number."""
    console.print(Panel(f"Fetching datasheet for [bold cyan]{mpn}[/bold cyan]...", title="datasheet-cli fetch"))
    console.print(f"[yellow]Target directory:[/yellow] {output_dir}")
    # TODO: Connect to distributor API or vendor fetcher
    console.print("[green]Ready to fetch.[/green]")


@app.command()
def parse(
    pdf_path: str = typer.Argument(..., help="Path to datasheet PDF"),
):
    """Scan a datasheet for 'Typical Application' diagrams, pinout tables, and design formulas."""
    console.print(Panel(f"Scanning [bold cyan]{pdf_path}[/bold cyan] for reference schematics...", title="datasheet-cli parse"))
    # TODO: Connect to PyMuPDF / Surya parser


@app.command()
def generate(
    mpn: str = typer.Argument(..., help="Manufacturer Part Number"),
    output: str = typer.Option("./output.kicad_sch", "--output", "-o", help="Output KiCad schematic path"),
    target_vout: float = typer.Option(3.3, "--vout", help="Target output voltage (V)"),
    target_vin: float = typer.Option(12.0, "--vin", help="Target input voltage (V)"),
):
    """Synthesize reference schematic into a KiCad schematic file."""
    console.print(Panel(f"Synthesizing circuit for [bold cyan]{mpn}[/bold cyan] (VIN={target_vin}V, VOUT={target_vout}V)", title="datasheet-cli generate"))
    console.print(f"[green]Target schematic:[/green] {output}")
    # TODO: Connect to solver and KiCad exporter


def main():
    app()


if __name__ == "__main__":
    main()
