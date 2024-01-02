from typing import Optional

import requests
from decouple import config
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from instagraper.cleaner import clean_posts
from instagraper.exceptions import InstagraperException
from instagraper.geojson import GeojsonBuilder
from instagraper.map import create_map
from instagraper.models import Post
from instagraper.utils import dump_posts

API_URL = "https://www.instagram.com/api/v1/feed/user/{user_id}/"
USERNAME_URL = "https://www.instagram.com/api/v1/feed/user/{username}/username"


def scrape(
    username: str,
    x_ig_app_id: Optional[str] = None,
    session_id: Optional[str] = None,
    compact: Optional[bool] = False,
    json_output: Optional[str] = None,
    geojson_output: Optional[str] = None,
    map_output: Optional[str] = None,
    with_images: Optional[bool] = False,
) -> list[dict | Post]:
    """
    Scrapes Instagram posts for a given username and performs optional data processing and output generation.

    Args:
        username (str): The Instagram username to scrape posts from.
        x_ig_app_id (str, optional): The Instagram app ID. Defaults to None.
        session_id (str, optional): The Instagram session ID. Defaults to None.
        compact (bool, optional): Flag indicating whether to clean up the scraped posts. Defaults to False.
        json_output (str, optional): The file path to save the scraped posts in JSON format. Defaults to None.
        geojson_output (str, optional): The file path to save the scraped posts in GeoJSON format. Defaults to None.
        map_output (str, optional): The file path to save the generated map. Defaults to None.
        with_images (bool, optional): Flag indicating whether to download and save images. Defaults to False.

    Returns:
        list[dict | Post]: The list of scraped posts, optionally cleaned up and processed.
    """

    scraper = Scraper(x_ig_app_id, session_id)
    posts = scraper.get_posts(username)
    image_dir = f"{username}/images" if with_images else None
    if geojson_output is None and map_output is not None:
        geojson_output = f"{username}.geojson"

    if geojson_output is not None:
        builder = GeojsonBuilder(posts, image_dir)
        geojson_posts = builder.get_geojson()
        dump_posts(username, geojson_posts, geojson_output)

    if compact:
        posts = list(clean_posts(posts))

    if json_output is not None:
        dump_posts(username, posts, json_output)

    if map_output is not None:
        create_map(map_output, geojson_output)

    return posts


class Scraper:
    _batch_count = 12

    def __init__(
        self, x_ig_app_id: Optional[str] = None, session_id: Optional[str] = None
    ) -> None:
        x_ig_app_id = x_ig_app_id or config("X_IG_APP_ID")
        session_id = session_id or config("SESSION_ID")
        self.headers = {"x-ig-app-id": x_ig_app_id}
        self.cookies = {"sessionid": session_id}

    def make_request(self, url: str, params: dict = {}) -> dict:
        response = requests.get(
            url, params=params, headers=self.headers, cookies=self.cookies
        )
        data = response.json()
        return data

    def get_user_id(self, username) -> str:
        print(f"\ngetting [bold green]{username}[/bold green] id")
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}")
        ) as progress:
            task = progress.add_task(
                description="fetching id...",
                total=None,
            )
            url = USERNAME_URL.format(username=username)
            data = self.make_request(url)
            if user := data.get("user"):
                if pk := user.get("pk"):
                    progress.update(
                        task,
                        description=f"got [bold green]{username}[/bold green] id: [bold magenta]{pk}[/bold magenta]",
                    )

                    return pk
        raise InstagraperException(
            "unable to connect to instagram API. did you provide the correct x-ig-app-id and session-id?"
        )

    def get_posts_chunk(self, url: str, max_id=None) -> list[dict]:
        params = {"count": str(self._batch_count)}
        if max_id is not None:
            params["max_id"] = max_id
        data = self.make_request(url, params)

        if data["status"] == "fail":
            raise InstagraperException(data["message"])

        if "items" not in data:
            return []

        items = data["items"]
        if len(items) == 0:
            return []

        return items

    def get_posts(self, username: str) -> list[dict]:
        user_id = self.get_user_id(username)
        url = API_URL.format(user_id=user_id)
        posts = []
        max_id = None
        print(f"\ngetting [bold green]{username}[/bold green] posts")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(description="fetching posts...", total=None)
            while True:
                try:
                    posts_chunk = self.get_posts_chunk(url, max_id)
                except InstagraperException as e:
                    print(f"[bold red]Error:[/bold red] {e}")
                    break
                if len(posts_chunk) == 0:
                    progress.update(
                        task,
                        description=f"got all posts: [bold green]{len(posts)}[/bold green]",
                    )
                    break
                max_id = posts_chunk[-1]["id"]
                posts.extend(posts_chunk)
                progress.update(
                    task,
                    description=f"got [bold yellow]{len(posts)}[/bold yellow] posts",
                )
            return posts
