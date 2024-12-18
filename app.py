import click
import debugpy

from src.sdr_app import SdrControlApp

@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode.")
def cli(debug: bool):
    if debug:
        debugpy.listen(("localhost", 5678))
        click.secho("Waiting for debugger to attach...", fg="yellow", bold=True)
        debugpy.wait_for_client()

    app = SdrControlApp()
    app.run()

if __name__ == '__main__':
    cli()