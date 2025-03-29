import typer
import os
from pathlib import Path
from app.processor import process_file
from app.graph import get_recent_emails, get_onedrive_files

app = typer.Typer()

INPUT_DIR = Path("inputs")

@app.command()
def process(file: str):
    """Process a single file (text or image) using Azure OpenAI"""
    if not os.path.exists(file):
        typer.echo(f"❌ File not found: {file}")
        raise typer.Exit(code=1)
    
    filename, result = process_file(file)

    typer.secho(f"\n✅ File processed and saved as: outputs/{filename}\n", fg=typer.colors.GREEN)
    typer.secho("📄 AI Response:\n", fg=typer.colors.CYAN, bold=True)
    typer.echo(result)
    typer.secho("\n🔄 Processing complete!\n", fg=typer.colors.BLUE)

@app.command()
def batch():
    """Batch process all files in the inputs/ directory"""
    if not INPUT_DIR.exists():
        typer.echo("⚠️ 'inputs/' directory does not exist.")
        raise typer.Exit(code=1)
    
    files = list(INPUT_DIR.glob("*.*"))
    if not files:
        typer.echo("⚠️ No files found in 'inputs/' directory.")
        return

    for file in files:
        try:
            filename, result = process_file(str(file))
            typer.secho(f"\n✅ Processed: {file.name} → outputs/{filename}", fg=typer.colors.GREEN)
            typer.secho("📄 AI Response:\n", fg=typer.colors.CYAN, bold=True)
            typer.echo(result)
            typer.echo("-" * 80)
        except Exception as e:
            typer.secho(f"❌ Error processing {file.name}: {e}", fg=typer.colors.RED)

@app.command()
def read_emails():
    """Read last 5 emails using Microsoft Graph API"""
    emails = get_recent_emails()
    if not emails:
        typer.echo("⚠️ No emails found or unable to connect.")
        return
    for email in emails[:5]:
        print(f"📧 {email.get('subject')}")

@app.command()
def read_onedrive():
    """Read files from user's OneDrive using Microsoft Graph API"""
    files = get_onedrive_files()
    if not files:
        typer.echo("⚠️ No files found or unable to connect.")
        return
    for file in files[:5]:
        print(f"📂 {file.get('name')}")

if __name__ == "__main__":
    app()
