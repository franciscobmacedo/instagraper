import os
from dataclasses import asdict
from typing import Optional

import requests
from rich.progress import track

from instagraper.cleaner import clean_post
from instagraper.models import Post


class GeojsonBuilder:
    images_dir = "images"

    def __init__(
        self,
        posts: dict,
        target: str,
        with_images: bool,
        static_url: str,
    ) -> None:
        self.posts = posts
        self.target = target
        self.with_images = with_images
        self.static_url = static_url

    @property
    def images_path(self) -> Optional[str]:
        if self.with_images:
            _image_path = os.path.join(self.target, self.images_dir)
            os.makedirs(_image_path, exist_ok=True)
            return _image_path

    def get_geojson(self) -> dict:
        features = list(self.posts_to_point())
        geojson = {"type": "FeatureCollection", "features": features}
        return geojson

    def posts_to_point(self) -> dict:
        if self.with_images:
            message = "converting posts to geojson points and downloading images..."
        else:
            message = "converting posts to geojson points..."
        for post in track(self.posts, message):
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
        if self.with_images:
            image_file = self.get_image(post)

            if self.static_url:
                image_path = os.path.join(self.static_url, self.images_path, image_file)
            else:
                image_path = os.path.join(self.images_dir, image_file)

            content += f"""
                <img src="{image_path}" alt="{post.pk}" height="300" >
                """
            return content

    def get_image(self, post: Post) -> str:
        image_file = f"{post.pk}.webp"
        image_path = os.path.join(self.images_path, image_file)
        if not os.path.exists(image_path):
            r = requests.get(post.image_url)
            with open(image_path, "wb") as f:
                f.write(r.content)
        return image_file
