from instagraper.utils import dump_posts, write_json


def test_write_json(mocker):
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    # scrape(username, json_output="output.json")
    write_json(
        {"status": "success"},
        "output.json",
    )
    mock_open.assert_called_once_with("output.json", "w")


def test_dump_posts(mocker):
    username = "test_user"
    posts = [{"id": 1, "title": "Post 1"}, {"id": 2, "title": "Post 2"}]
    json_output = "output.json"

    mock_print = mocker.patch("instagraper.utils.print")
    mock_progress = mocker.patch("instagraper.utils.Progress")
    mock_write_json = mocker.patch("instagraper.utils.write_json")

    dump_posts(username, posts, json_output)

    mock_print.assert_called_with(
        f"\nwriting [bold green]{username}[/bold green] posts to [bold magenta]{json_output}[/bold magenta]"
    )

    mock_progress.assert_called_once_with(
        mocker.ANY,
        mocker.ANY,
    )

    mock_progress.return_value.__enter__.return_value.add_task.assert_called_once_with(
        description="writing ...", total=None
    )

    mock_write_json.assert_called_once_with(posts, json_output)

    mock_progress.return_value.__enter__.return_value.update.assert_called_once_with(
        mocker.ANY,
        description=f"wrote [bold green]{username}[/bold green] posts to [bold magenta]{json_output}[/bold magenta]",
    )
