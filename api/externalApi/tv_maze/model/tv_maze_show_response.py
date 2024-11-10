from typing import Optional

from pydantic import BaseModel


class TvMazeShowResponse(BaseModel):
    tv_show_id: int
    tv_show_name: str
    tv_show_url: str
    tv_show_image_original_url: Optional[str] = None





