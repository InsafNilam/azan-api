from sqlmodel import create_engine, Session
from app.database import init_db
from app.scripts.database import reset_database, seed_database
import typer

app = typer.Typer()

@app.command()
def migrate_fresh():
    """Drop and recreate database schema"""
    confirm = typer.confirm("Are you sure you want to reset the database?")
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Abort()
    
    reset_database()
    init_db()
    typer.echo("✅ Database schema reset successfully!")


@app.command()
def migrate_fresh_seed():
    """Reset database and seed with initial data"""
    confirm = typer.confirm("Are you sure you want to reset and seed the database?")
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Abort()

    reset_database()
    init_db()
    
    with Session(create_engine("sqlite:///database.db")) as session:
        seed_database(session)
    
    typer.echo("✅ Database reset and seeded successfully!")


if __name__ == "__main__":
    app()