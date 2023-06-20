from setup import __version__
import click


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Print the version number."""
    click.echo(f"AICodeBot version {__version__}")


if __name__ == "__main__":
    cli()
