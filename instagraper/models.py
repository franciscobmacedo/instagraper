from dataclasses import dataclass
from typing import Optional


@dataclass
class Post:
    taken_at: int
    pk: str
    id: str
    code: str
    user_id: str
    username: str
    user_full_name: str
    caption: Optional[str] = None
    location_pk: Optional[str] = None
    location_name: Optional[str] = None
    image_url: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

    @property
    def post_url(self):
        return f"https://www.instagram.com/p/{self.code}/"
