import click
from src.services.db_service import DatabaseService
from src.config import DATABASE_URL, get_db_path

@click.group()
def cli():
    pass

@cli.command()
@click.option('--url', required=True, help='Article URL')
def get_article(url):
    db_service = DatabaseService(DATABASE_URL)
    article = db_service.get_article_by_url(url)
    if article:
        click.echo(f"Found article: {article.url}")
        click.echo(f"Category: {article.category}")
        click.echo(f"Tags: {article.tags}")
    else:
        click.echo("Article not found")

@cli.command()
def db_info():
    """Get database connection information"""
    click.echo(f"Database Path: {get_db_path()}")
    click.echo(f"Database URL: {DATABASE_URL}")

cli.add_command(get_article)
cli.add_command(db_info)

if __name__ == '__main__':
    cli() 