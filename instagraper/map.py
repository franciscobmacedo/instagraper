import os
from pathlib import Path

from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

INSTAGRAPER_DIR = Path(__file__).parent


def create_map(map_output: str, geojson_output: str, target: str):
    print(f"\nCreating map at [bold green]{map_output}[/bold green]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(description="writing ...", total=None)
        template_path = os.path.join(INSTAGRAPER_DIR, "templates", "map.html")
        with open(template_path) as f:
            map_template = f.read()

        map_template = map_template.replace("{{data_file}}", geojson_output)
        with open(os.path.join(target, map_output), "w") as f:
            f.write(map_template)

        progress.update(
            task,
            description=f"wrote map [bold green]{map_output}[/bold green]",
        )
