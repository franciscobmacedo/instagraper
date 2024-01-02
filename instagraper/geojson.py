import os
from dataclasses import asdict
from typing import Optional

import requests
from rich.progress import track

from instagraper.cleaner import clean_post
from instagraper.models import Post


class GeojsonBuilder:
    def __init__(
        self, posts: dict, image_dir: str = None, base_url: str = None
    ) -> None:
        self.posts = posts
        self.image_dir = image_dir
        if self.image_dir:
            os.makedirs(image_dir, exist_ok=True)
        self.base_url = base_url

    def get_geojson(self) -> dict:
        features = list(self.posts_to_point())
        geojson = {"type": "FeatureCollection", "features": features}
        return geojson

    def posts_to_point(self) -> dict:
        for post in track(self.posts, "converting posts to geojson points..."):
            point = self.post_to_point(post)
            if point:
                yield point

    def post_to_point(self, raw_post: dict) -> Optional[dict]:
        post = clean_post(raw_post)

        if not post.lat or not post.lng:
            return None
        description = self.get_description(post)
        point = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [post.lng, post.lat],
            },
            "properties": {
                "description": description,
                "clean": asdict(post),
                "raw": raw_post,
            },
        }
        return point

    def get_description(self, post: Post) -> str:
        content = f"""
        <a href={post.post_url} target="_blank"><h2>{post.location_name or 'see post'}</h2></a>
        <p>{post.caption}</p>
        """
        image_path = self.get_image(post)
        if image_path:
            content += f"""
                <img src="{image_path}" alt="{post.pk}" height="300" >
                """
        return content

    def get_image(self, post: Post) -> Optional[str]:
        if self.image_dir is None:
            return
        image_path = os.path.join(self.image_dir, f"{post.pk}.webp")
        if not os.path.exists(image_path):
            r = requests.get(post.image_url)
            with open(image_path, "wb") as f:
                f.write(r.content)
        if self.base_url is not None:
            image_path = os.path.join(self.base_url, image_path)
        return image_path
