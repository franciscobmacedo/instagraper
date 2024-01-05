from typing import Annotated

import typer

from instagraper import scraper

app = typer.Typer()


@app.command()
def scrape(
    username: Annotated[
        str, typer.Argument(help="The Instagram username to scrape posts from.")
    ],
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
        typer.Option("--compact", "-c", help="Wether to cleanup the scraped posts"),
    ] = True,
    json_output: Annotated[
        str,
        typer.Option(
            "--json",
            "-j",
            help="The file name to save the scraped posts in JSON format. The file path will be {target}/{json_output}.",
        ),
    ] = None,
    geojson_output: Annotated[
        str,
        typer.Option(
            "--geojson",
            "-g",
            help="The file name to save the scraped posts in GeoJSON format. If map is enabled, it will be used as the input file for the map and will default to {username}.geojson. The file path will be {target}/{geojson_output}.",
        ),
    ] = None,
    map_output: Annotated[
        str,
        typer.Option(
            "--map",
            "-m",
            help="The html file name to save the generated map. The file path will be {target}/{map_output}.",
        ),
    ] = None,
    target: Annotated[
        str,
        typer.Option(
            "--target",
            "-t",
            help="the target path/directory to save the output files. Defaults to a directory with the instagram username as it's name, e.g ./{username}/",
        ),
    ] = None,
    with_images: Annotated[
        bool,
        typer.Option(
            "--images",
            "-i",
            help="whether to download post's images or not. The images will be saved in the {target}/images directory.",
        ),
    ] = False,
    static_url: Annotated[
        str,
        typer.Option(
            "--static-url",
            "-s",
            help="The static url/path where the target directory will be hosted. Used to serve the images for the geojson output. e.g. if https://example.com/instagraper/ images will be in https://example.com/instagraper/{target}/images/",
        ),
    ] = None,
    limit: Annotated[
        int,
        typer.Option(
            "--limit",
            "-l",
            help="The maximum number of posts to scrape. If not provided, all posts will be scraped.",
        ),
    ] = None,
):
    """
    Scrape Instagram profile posts and corresponding locations
    """

    scraper.scrape(
        username=username,
        x_ig_app_id=x_ig_app_id,
        session_id=session_id,
        compact=compact,
        json_output=json_output,
        geojson_output=geojson_output,
        map_output=map_output,
        target=target,
        with_images=with_images,
        static_url=static_url,
        limit=limit,
    )
