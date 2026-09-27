"""
Inditex Analytics CLI — professional command-line interface.

Usage:
    python cli.py report            # Financial report
    python cli.py brands            # Sales by brand
    python cli.py abc               # ABC analysis
    python cli.py regions           # Geographic distribution
    python cli.py growth            # Growth rankings
    python cli.py --help            # Show help
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from db import run_query

app = typer.Typer(
    name="inditex",
    help="🛍️  Inditex Analytics — business intelligence from the command line",
    add_completion=False,
)

console = Console()


# ============================================================
# HEADER
# ============================================================
def print_header():
    text = Text()
    text.append("🛍️  ", style="bold")
    text.append("INDITEX ANALYTICS", style="bold white")
    text.append("  ·  ", style="dim")
    text.append("Business Intelligence CLI", style="italic cyan")
    console.print(Panel(text, border_style="cyan", padding=(0, 2)))


# ============================================================
# COMMAND: report
# ============================================================
@app.command()
def report(year: int = typer.Option(2025, help="Financial year to report")):
    """📊 Show financial report for a given year."""
    print_header()
    console.print(f"\n[bold cyan]📅 Financial Report — {year}[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Querying database...", total=None)
        df = run_query(f"SELECT * FROM financials WHERE year = {year};")
        progress.update(task, completed=True)

    if df.empty:
        console.print(f"[red]No data for year {year}.[/red]")
        return

    row = df.iloc[0]

    table = Table(show_header=False, border_style="cyan", padding=(0, 2))
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right", style="bold white")

    table.add_row("💰 Revenue", f"€{row['revenue_millions']:,.0f}M")
    table.add_row("📈 Net Income", f"€{row['net_income_millions']:,.0f}M")
    table.add_row("📊 Gross Margin", f"{row['gross_margin_pct']:.2f}%")
    table.add_row("🏬 Stores", f"{row['stores_count']:,}")
    table.add_row("🌍 Countries", f"{row['countries_count']:,}")

    console.print(table)

    # YoY growth
    prev = run_query(f"SELECT * FROM financials WHERE year < {year} ORDER BY year DESC LIMIT 1;")
    if not prev.empty:
        prev_rev = prev.iloc[0]["revenue_millions"]
        yoy = (row["revenue_millions"] - prev_rev) / prev_rev * 100
        color = "green" if yoy >= 0 else "red"
        sign = "+" if yoy >= 0 else ""
        console.print(f"\n[{color}]YoY revenue growth: {sign}{yoy:.2f}%[/{color}]")


# ============================================================
# COMMAND: brands
# ============================================================
@app.command()
def brands():
    """🏷️  Show sales by brand."""
    print_header()
    console.print("\n[bold cyan]🏷️  Sales by Brand — 2025[/bold cyan]\n")

    df = run_query("""
        SELECT b.brand_name, s.sales_millions, s.growth_pct
        FROM sales_by_brand s
        JOIN brands b ON s.brand_id = b.brand_id
        ORDER BY s.sales_millions DESC;
    """)

    table = Table(border_style="cyan", header_style="bold cyan")
    table.add_column("Brand", style="bold")
    table.add_column("Sales (€M)", justify="right")
    table.add_column("Growth", justify="right")

    total = df["sales_millions"].sum()

    for _, row in df.iterrows():
        pct = row["sales_millions"] / total * 100
        growth_color = "green" if row["growth_pct"] >= 10 else "yellow" if row["growth_pct"] >= 3 else "red"
        table.add_row(
            row["brand_name"],
            f"€{row['sales_millions']:,.0f}M  ({pct:.1f}%)",
            f"[{growth_color}]+{row['growth_pct']:.1f}%[/{growth_color}]",
        )

    console.print(table)
    console.print(f"\n[dim]Total: €{total:,.0f}M[/dim]")


# ============================================================
# COMMAND: abc
# ============================================================
@app.command()
def abc():
    """📊 Run ABC analysis on brands."""
    print_header()
    console.print("\n[bold cyan]📊 ABC Analysis — Brand Portfolio[/bold cyan]\n")

    df = run_query("""
        SELECT b.brand_name, s.sales_millions
        FROM sales_by_brand s
        JOIN brands b ON s.brand_id = b.brand_id
        ORDER BY s.sales_millions DESC;
    """)

    df["cumulative_pct"] = df["sales_millions"].cumsum() / df["sales_millions"].sum() * 100
    df["class"] = df["cumulative_pct"].apply(
        lambda x: "A" if x <= 80 else "B" if x <= 95 else "C"
    )

    table = Table(border_style="cyan", header_style="bold cyan")
    table.add_column("Class", justify="center")
    table.add_column("Brand", style="bold")
    table.add_column("Sales (€M)", justify="right")
    table.add_column("Cumulative %", justify="right")

    class_colors = {"A": "green", "B": "yellow", "C": "red"}

    for _, row in df.iterrows():
        cls = row["class"]
        color = class_colors[cls]
        table.add_row(
            f"[{color}]{cls}[/{color}]",
            row["brand_name"],
            f"€{row['sales_millions']:,.0f}M",
            f"{row['cumulative_pct']:.2f}%",
        )

    console.print(table)
    console.print("\n[bold]Legend:[/bold]")
    console.print("  [green]A[/green] = Top 80% of sales (core portfolio)")
    console.print("  [yellow]B[/yellow] = 80-95% (secondary)")
    console.print("  [red]C[/red] = 95-100% (long tail)")


# ============================================================
# COMMAND: regions
# ============================================================
@app.command()
def regions():
    """🌍 Show sales distribution by region."""
    print_header()
    console.print("\n[bold cyan]🌍 Geographic Distribution — 2025[/bold cyan]\n")

    df = run_query("SELECT * FROM sales_by_region ORDER BY sales_pct DESC;")

    table = Table(border_style="cyan", header_style="bold cyan")
    table.add_column("Region", style="bold")
    table.add_column("Share", justify="right")

    for _, row in df.iterrows():
        bar_len = int(row["sales_pct"] / 2)
        bar = "█" * bar_len
        table.add_row(
            row["region"],
            f"[cyan]{bar}[/cyan] {row['sales_pct']:.2f}%",
        )

    console.print(table)


# ============================================================
# COMMAND: growth
# ============================================================
@app.command()
def growth():
    """📈 Show growth ranking by brand."""
    print_header()
    console.print("\n[bold cyan]📈 Growth Ranking — 2025[/bold cyan]\n")

    df = run_query("""
        SELECT b.brand_name, s.sales_millions, s.growth_pct
        FROM sales_by_brand s
        JOIN brands b ON s.brand_id = b.brand_id
        ORDER BY s.growth_pct DESC;
    """)

    table = Table(border_style="cyan", header_style="bold cyan")
    table.add_column("#", justify="center")
    table.add_column("Brand", style="bold")
    table.add_column("Growth", justify="right")
    table.add_column("Size (€M)", justify="right")

    for i, (_, row) in enumerate(df.iterrows(), 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        color = "green" if row["growth_pct"] >= 10 else "yellow" if row["growth_pct"] >= 3 else "red"
        table.add_row(
            medal,
            row["brand_name"],
            f"[{color}]+{row['growth_pct']:.2f}%[/{color}]",
            f"€{row['sales_millions']:,.0f}M",
        )

    console.print(table)


# ============================================================
# COMMAND: ask (AI agent)
# ============================================================
@app.command()
def ask(
    question: str = typer.Argument(..., help="Ask a question in natural language"),
    show_sql: bool = typer.Option(False, "--sql", help="Show the generated SQL"),
):
    """🤖 Perguntar em linguagem natural (agente IA SQL)."""
    from agent import ask as agent_ask

    print_header()
    console.print(f"\n[bold cyan]🤖 Pergunta:[/bold cyan] {question}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("A gerar SQL e a consultar a base de dados...", total=None)
        response = agent_ask(question)
        progress.update(task, completed=True)

    if "error" in response:
        console.print(f"[red]Erro: {response['error']}[/red]")
        if show_sql:
            console.print(f"\n[dim]SQL: {response['sql']}[/dim]")
        return

    # Show plan
    if "plan" in response:
        console.print(Panel(
            response["plan"],
            title="[bold yellow]🧠 Agent Plan[/bold yellow]",
            border_style="yellow",
            padding=(0, 2),
        ))

    # Show SQL
    if show_sql:
        console.print(Panel(
            response["sql"],
            title="[dim]🔍 Generated SQL[/dim]",
            border_style="dim",
            padding=(0, 2),
        ))

    # Result table
    if not response["result"].empty:
        df = response["result"]
        table = Table(border_style="cyan", header_style="bold cyan")
        for col in df.columns:
            table.add_column(str(col), justify="right" if df[col].dtype != object else "left")
        for _, row in df.iterrows():
            table.add_row(*[str(v) for v in row.values])
        console.print(table)

    console.print(f"\n[bold green]💡 Answer:[/bold green] {response['explanation']}")

    # Attempt info
    if "attempts" in response and response["attempts"] > 1:
        console.print(f"\n[yellow]🔄 Required {response['attempts']} attempts (auto-corrected)[/yellow]")

    if "duration_ms" in response and response["duration_ms"]:
        console.print(f"[dim]⏱️  Executed in {response['duration_ms']} ms[/dim]")

    # Follow-up suggestions
    if "followups" in response and response["followups"]:
        console.print("\n[bold cyan]💭 You may also ask:[/bold cyan]")
        for f in response["followups"]:
            console.print(f"  [dim]•[/dim] {f}")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app()






