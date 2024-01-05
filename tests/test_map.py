from instagraper.map import create_map


def test_create_map(mocker):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.map.open", mock_open)

    map_output = "map.html"
    geojson_output = "output.geojson"

    create_map(map_output, geojson_output, "test")

    mock_open.assert_called_with("test/map.html", "w")
    mock_open.return_value.__enter__.return_value.read.assert_called_once()

    assert mock_open.call_count == 2
    assert mock_open.return_value.__enter__.return_value.write.call_count == 1
