import pytest

from instagraper.models import Post
from instagraper.scraper import API_URL, USERNAME_URL, scrape


@pytest.fixture
def scraper_request_fixture(mocker, requests_mock):
    posts = [
        {
            "taken_at": 123456789,
            "pk": "aaa",
            "id": "aaa_12345",
            "code": "abc123",
            "user": {
                "id": "12345",
                "username": "example_user",
                "full_name": "Example User",
            },
            "caption": {
                "text": "Example caption",
            },
            "location": {
                "pk": "12345",
                "name": "Example location",
                "lat": 12.345,
                "lng": 12.345,
            },
            "image_versions2": {
                "candidates": [
                    {
                        "url": "https://example.com/image.jpg",
                    }
                ]
            },
        },
        {
            "taken_at": 987654321,
            "pk": "bbb",
            "id": "bbb_54321",
            "code": "abc456",
            "user": {
                "id": "12345",
                "username": "example_user",
                "full_name": "Example User",
            },
            "caption": {
                "text": "Example caption",
            },
            "location": {
                "pk": "12345",
                "name": "Example location",
                "lat": 12.345,
                "lng": 12.345,
            },
            "image_versions2": {
                "candidates": [
                    {
                        "url": "https://example.com/image.jpg",
                    }
                ]
            },
        },
    ]
    username = "example_user"
    user_id = "12345"
    requests_mock.get(
        USERNAME_URL.format(username=username), json={"user": {"pk": user_id}}
    )
    requests_mock.get(
        API_URL.format(user_id=user_id) + "?count=12",
        json={"status": "success", "items": posts},
    )
    requests_mock.get(
        API_URL.format(user_id=user_id) + "?count=12&max_id=bbb_54321",
        json={
            "status": "fail",
            "message": "No more posts",
        },
    )
    requests_mock.get(
        "https://example.com/image.jpg",
        content=b"image",
    )

    mocker.patch("instagraper.scraper.os.makedirs", mocker.mock_open())


def test_scrape_with_json_output(mocker, scraper_request_fixture):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.utils.open", mock_open)
    posts = scrape(
        x_ig_app_id="test-app-id",
        session_id="test-session-id",
        username="example_user",
        json_output="output.json",
    )
    mock_open.assert_called_once_with("example_user/output.json", "w")
    assert len(posts) == 2


def test_scrape_with_geojson_output(mocker, scraper_request_fixture):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.utils.open", mock_open)
    posts = scrape(
        x_ig_app_id="test-app-id",
        session_id="test-session-id",
        username="example_user",
        geojson_output="output.geojson",
        with_images=False,
    )
    mock_open.assert_called_once_with("example_user/output.geojson", "w")
    assert len(posts) == 2


def test_scrape_with_compact_option(scraper_request_fixture):
    posts = scrape(
        x_ig_app_id="test-app-id",
        session_id="test-session-id",
        username="example_user",
        compact=True,
    )
    assert len(posts) == 2
    assert isinstance(posts[0], Post)


def test_scrape_with_map_output(mocker, scraper_request_fixture):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.template.open", mock_open)
    mocker.patch("instagraper.utils.open", mock_open)
    posts = scrape(
        x_ig_app_id="test-app-id",
        session_id="test-session-id",
        username="example_user",
        map_output="map.html",
        with_images=False,
    )
    mock_open.assert_any_call("example_user/map.html", "w")
    mock_open.assert_any_call("example_user/example_user.geojson", "w")
    assert len(posts) == 2


def test_scrape_with_images(mocker, scraper_request_fixture):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.utils.open", mock_open)
    mocker.patch("instagraper.geojson.open", mock_open)

    posts = scrape(
        x_ig_app_id="test-app-id",
        session_id="test-session-id",
        username="example_user",
        geojson_output="output.geojson",
        with_images=True,
    )
    mock_open.assert_called_with("example_user/output.geojson", "w")
    mock_open.assert_any_call("example_user/images/aaa.webp", "wb")
    mock_open.assert_any_call("example_user/images/bbb.webp", "wb")
    assert len(posts) == 2


def test_scrape_with_custom_target_directory(mocker, scraper_request_fixture):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.utils.open", mock_open)
    mocker.patch("instagraper.template.open", mock_open)
    mocker.patch("instagraper.geojson.open", mock_open)

    posts = scrape(
        x_ig_app_id="test-app-id",
        session_id="test-session-id",
        username="example_user",
        target="example/target/directory",
        map_output="output.html",
        with_images=True,
    )
    mock_open.assert_any_call("example/target/directory/example_user.geojson", "w")
    mock_open.assert_any_call("example/target/directory/output.html", "w")
    mock_open.assert_any_call("example/target/directory/images/aaa.webp", "wb")
    mock_open.assert_any_call("example/target/directory/images/bbb.webp", "wb")
    assert len(posts) == 2
