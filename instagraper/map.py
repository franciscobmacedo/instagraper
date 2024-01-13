from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from instagraper.template import Template


def create_map(geojson_output: str, output: str, username: str):
    print(f"\nCreating map at [bold green]{output}[/bold green]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(description="writing ...", total=None)
        context = {
            "data_file": geojson_output,
            "title": f"{username} Map",
        }
        template = Template(output=output)
        content = template.render(context=context)
        template.dump(content)
        progress.update(
            task,
            description=f"wrote map [bold green]{output}[/bold green]",
        )
