from pydantic import BaseModel, Field


class PlaylistName(BaseModel):
    title: str = Field(..., description="Short, catchy playlist title")
    subtitle: str | None = Field(None, description="Optional subtitle or tagline that adds flavor")
    rationale: str = Field(
        ..., description="1-2 sentence explanation tying the title to the inputs"
    )


class PlaylistSuggestions(BaseModel):
    names: list[PlaylistName] = Field(..., description="List of suggested playlist names")
