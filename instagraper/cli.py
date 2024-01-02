from typing import Annotated

import typer

from instagraper import scraper

app = typer.Typer()


@app.command()
def scrape(
    username: Annotated[str, typer.Argument(help="The instagram username")],
    x_ig_app_id: Annotated[
        str,
        typer.Option(
            help="Instagram app id (x-ig-app-id) header to authenticate the requests. If not provided, the tool will try to read it from the environment variable X_IG_APP_ID",
        ),
    ] = None,
    session_id: Annotated[
        str,
        typer.Option(
            help="Instagram session id (sessionid) cookie to authenticate the requests. If not provided, the tool will try to read it from the environment variable SESSION_ID",
        ),
    ] = None,
    compact: Annotated[
        bool,
        typer.Option(
            "--compact", "-c", help="wether to compact the JSON output or not"
        ),
    ] = True,
    with_json: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="whether to dump the posts to a JSON file or not.",
        ),
    ] = False,
    with_geojson: Annotated[
        bool,
        typer.Option(
            "--geojson",
            "-g",
            help="whether to dump the posts to a GeoJSON file or not. If map is enabled, this will be enabled by default.",
        ),
    ] = False,
    with_map: Annotated[
        bool,
        typer.Option(
            "--map",
            "-m",
            help="whether to create a map with the posts or not. It will enable GeoJSON output by default.",
        ),
    ] = False,
    with_images: Annotated[
        bool,
        typer.Option(
            "--images",
            "-i",
            help="whether to download post's images or not.",
        ),
    ] = False,
):
    """
    Scrape Instagram profile posts and corresponding locations
    """
    json_output = f"{username}.json" if with_json else None
    geojson_output = f"{username}.geojson" if with_geojson else None
    map_output = f"{username}.html" if with_map else None
    print("json", json_output)
    scraper.scrape(
        username=username,
        x_ig_app_id=x_ig_app_id,
        session_id=session_id,
        compact=compact,
        json_output=json_output,
        geojson_output=geojson_output,
        map_output=map_output,
        with_images=with_images,
    )
