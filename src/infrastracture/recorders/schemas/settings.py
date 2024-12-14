from pydantic import BaseModel, Field

from infrastracture.recorders.schemas.resolution import Resolution


class Settings(BaseModel):
    fps: int = Field(le=1)
    resolution: Resolution


class SetSettings(Settings):
    fps: int | None = Field(default=None, le=1)
    resolution: Resolution | None = None

    @property
    def empty(self) -> bool:
        return self.fps is None and self.resolution is None
