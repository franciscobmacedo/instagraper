import json
from dataclasses import asdict
from typing import Union

from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from instagraper.models import Post


def dump_posts(
    username: str, posts: Union[dict, list[dict], list[Post]], json_output: str
) -> None:
    if isinstance(posts, list) and len(posts) > 0 and isinstance(posts[0], Post):
        posts = [asdict(post) for post in posts]
    print(
        f"\nwriting [bold green]{username}[/bold green] posts to [bold magenta]{json_output}[/bold magenta]"
    )
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(description="writing ...", total=None)
        write_json(posts, json_output)

        progress.update(
            task,
            description=f"wrote [bold green]{username}[/bold green] posts to [bold magenta]{json_output}[/bold magenta]",
        )


def write_json(data, filename="data.json") -> None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4, default=str)


def read_json(filename="data.json") -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data
