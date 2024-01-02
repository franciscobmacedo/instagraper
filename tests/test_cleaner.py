import datetime

import pytest

from instagraper.cleaner import clean_post
from instagraper.models import Post


def test_clean_post_with_location():
    post = {
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
    }

    expected_post = Post(
        taken_at=datetime.datetime.fromtimestamp(123456789),
        pk="aaa",
        id="aaa_12345",
        code="abc123",
        user_id="12345",
        username="example_user",
        user_full_name="Example User",
        caption="Example caption",
        location_pk="12345",
        location_name="Example location",
        lat=12.345,
        lng=12.345,
        image_url="https://example.com/image.jpg",
    )

    cleaned_post = clean_post(post)
    assert cleaned_post == expected_post


def test_clean_post_without_location():
    post = {
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
        "image_versions2": {
            "candidates": [
                {
                    "url": "https://example.com/image.jpg",
                }
            ]
        },
    }

    expected_post = Post(
        taken_at=datetime.datetime.fromtimestamp(987654321),
        pk="bbb",
        id="bbb_54321",
        code="abc456",
        user_id="12345",
        username="example_user",
        user_full_name="Example User",
        caption="Example caption",
        image_url="https://example.com/image.jpg",
    )

    cleaned_post = clean_post(post)
    assert cleaned_post == expected_post


def test_clean_post_with_wrong_data():
    post = {
        "taken_at": "123456789",  # Invalid data type for taken_at
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
    }

    with pytest.raises(Exception):
        # Expecting Exception due to Invalid data type for 'taken_at' field
        clean_post(post)


def test_clean_post_with_missing_fields():
    post = {
        "taken_at": 123456789,
        "pk": "aaa",
        "id": "aaa_12345",
        # Missing 'code' field
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
    }

    with pytest.raises(Exception):
        # Expecting Exception due to missing 'code' field
        clean_post(post)
