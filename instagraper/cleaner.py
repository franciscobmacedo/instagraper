import datetime
from typing import Optional

from instagraper.models import Post


def clean_posts(posts: list[dict]) -> list[Post]:
    for post in posts:
        yield clean_post(post)


def clean_post(post: dict) -> Post:
    cleaned_post = {}
    cleaned_post["taken_at"] = datetime.datetime.fromtimestamp(post["taken_at"])
    cleaned_post["pk"] = post["pk"]
    cleaned_post["id"] = post["id"]
    cleaned_post["code"] = post["code"]

    user = post["user"]
    cleaned_post["user_id"] = user["id"]
    cleaned_post["username"] = user["username"]
    cleaned_post["user_full_name"] = user["full_name"]

    if caption := post.get("caption", None):
        cleaned_post["caption"] = caption["text"]

    location: Optional[dict] = post.get("location", None)
    if location:
        cleaned_post["location_pk"] = location["pk"]
        cleaned_post["location_name"] = location["name"]
        cleaned_post["lat"] = location.get("lat", None)
        cleaned_post["lng"] = location.get("lng", None)

    cleaned_post["image_url"] = post["image_versions2"]["candidates"][0]["url"]
    return Post(**cleaned_post)
