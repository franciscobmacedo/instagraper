import os
from pathlib import Path

INSTAGRAPER_DIR = Path(__file__).parent


def load_template() -> str:
    template_path = os.path.join(INSTAGRAPER_DIR, "templates", "map.html")
    with open(template_path) as f:
        map_template = f.read()
    return map_template


class Template:
    def __init__(self, output: str) -> None:
        self.output = output

    def render(self, context: dict) -> str:
        map_template = load_template()
        for key, value in context.items():
            map_template = map_template.replace(f"{{{{{key}}}}}", value)
        return map_template

    def dump(self, content: str) -> str:
        with open(self.output, "w") as f:
            f.write(content)
