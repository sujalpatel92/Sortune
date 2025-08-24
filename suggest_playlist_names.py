import json
import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama  # Local Ollama backend
from langchain_openai import ChatOpenAI  # OpenAI GPT backend
from pydantic import BaseModel, Field

load_dotenv()


# --------- Output schema ---------
class PlaylistName(BaseModel):
    title: str = Field(..., description="Short, catchy playlist title")
    subtitle: str | None = Field(None, description="Optional subtitle or tagline that adds flavor")
    rationale: str = Field(
        ..., description="1-2 sentence explanation tying the title to the inputs"
    )


class PlaylistSuggestions(BaseModel):
    names: list[PlaylistName] = Field(..., description="List of suggested playlist names")


# --------- Prompt + Parser ---------
parser = JsonOutputParser(pydantic_object=PlaylistSuggestions)

SYSTEM = """You are a sharp, creative music curator who generates sleek playlist titles.
Blend artist/album vibes with the given date/season. Avoid cheesy puns unless asked.
If you think you have not heard of an artist/album, search the internet to find
more information about it.
Keep titles concise (2-5 words when possible). Do NOT invent fake artists or albums."""

USER = """Generate {count} playlist names.

Inputs:
- Artists: {artists}
- Albums: {albums}
- Date context: {date}

Style constraints:
- Tone: {tone}
- Audience: {audience}
- Must avoid duplicate or near-duplicate titles.
- Titles should be timeless (work on streaming platforms).
- If seasonal cues apply from the date, you may weave them in subtly.

{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([("system", SYSTEM), ("user", USER)]).partial(
    format_instructions=parser.get_format_instructions()
)


# --------- Chain builder ---------
def build_playlist_chain(
    backend: str = "openai",
    model: str = "gpt-4o-mini",  # change to your preferred OpenAI model, or an Ollama model name
    temperature: float = 0.9,
):
    """
    backend: 'openai' or 'ollama'
    model:   OpenAI model name (e.g., 'gpt-4o', 'gpt-4.1') or Ollama model (e.g., 'llama3:8b')
    """
    if backend == "openai":
        llm = ChatOpenAI(model=model, temperature=temperature)
    elif backend == "ollama":
        llm = ChatOllama(model=model, temperature=temperature)
    else:
        raise ValueError("backend must be 'openai' or 'ollama'")

    chain = prompt | llm | parser
    return chain


# --------- Convenience wrapper ---------
def suggest_playlist_names(
    artists: list[str],
    albums: list[str],
    date: str,
    count: int = 10,
    tone: str = "modern, sleek, slightly moody",
    audience: str = "general streaming listeners",
    backend: str = "openai",
    model: str = "gpt-4o-mini",
    temperature: float = 0.9,
) -> PlaylistSuggestions:
    """
    Returns a PlaylistSuggestions pydantic object with structured results.
    """
    chain = build_playlist_chain(backend=backend, model=model, temperature=temperature)
    return chain.invoke(
        {
            "artists": ", ".join(artists),
            "albums": ", ".join(albums),
            "date": date,
            "count": count,
            "tone": tone,
            "audience": audience,
        }
    )


def get_data_from_cache(cache_file_name: str) -> list[dict[str, Any]]:
    if not os.path.exists(os.path.join("cache", cache_file_name)):
        return None
    filepath = os.path.join("cache", cache_file_name)
    with open(filepath) as f:
        return json.load(f)


# --------- Example usage ---------
if __name__ == "__main__":
    albums_list = get_data_from_cache("albums.json")
    artists_list = get_data_from_cache("artists.json")

    albums = [album["title"] for album in albums_list]
    artists = [artist["artist"] for artist in artists_list]

    print(f"Albums:\n{albums}\n")
    print(f"Artists:\n{artists}\n")

    date = "August 23, 2025"

    # Use OpenAI (needs OPENAI_API_KEY env var)
    suggestions = suggest_playlist_names(
        artists,
        albums,
        date,
        count=8,
        tone="sleek, contemporary, minimal",
        audience="YouTube Music / Spotify users",
        backend="openai",
        model="gpt-5-nano",  # e.g., "gpt-4.1" or "gpt-4o"
        temperature=0.9,
    )
    print(suggestions)
    if not isinstance(suggestions, PlaylistSuggestions):
        suggestions = PlaylistSuggestions(**suggestions)

    # Or use local Ollama:
    # suggestions = suggest_playlist_names(
    #     artists,
    #     albums,
    #     date,
    #     count=8,
    #     backend="ollama",
    #     model="llama3:8b",  # or your preferred local model
    #     temperature=0.9,
    # )

    # Pretty print
    for i, n in enumerate(suggestions.names, 1):
        print(f"{i}. {n.title}")
        if n.subtitle:
            print(f"   — {n.subtitle}")
        print(f"   Why: {n.rationale}\n")
