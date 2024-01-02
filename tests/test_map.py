from instagraper.map import create_map


def test_create_map(mocker):
    mock_open = mocker.mock_open()
    mocker.patch("instagraper.map.open", mock_open)

    map_output = "map.html"
    geojson_output = "output.geojson"

    create_map(map_output, geojson_output)

    mock_open.assert_called_with("map.html", "w")
    mock_open.return_value.__enter__.return_value.read.assert_called_once()

    mock_open.assert_any_call(map_output, "w")
    mock_open.return_value.__enter__.return_value.write.assert_called_once()

    assert mock_open.call_count == 2
    assert mock_open.return_value.__enter__.return_value.write.call_count == 1
