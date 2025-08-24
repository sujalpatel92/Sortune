import json
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama  # Local Ollama backend
from langchain_openai import ChatOpenAI  # OpenAI GPT backend
from pydantic import BaseModel, Field
from ytmusicapi import OAuthCredentials, YTMusic

load_dotenv()

PLAYLIST_NAME = os.getenv("YT_PLAYLIST_NAME")
PLAYLIST_ID = os.getenv("YT_PLAYLIST_ID")
if not PLAYLIST_ID or not PLAYLIST_NAME:
    raise ValueError("Missing YT_PLAYLIST_ID or YT_PLAYLIST_NAME in environment")


# --------- Output schema ---------
class TagCategories(BaseModel):
    genre: list[str] = Field(default_factory=list, description="Genre or sub-genre tags")
    mood: list[str] = Field(default_factory=list, description="Mood/emotion tags")
    context: list[str] = Field(default_factory=list, description="Context/use-case tags")
    era: list[str] = Field(default_factory=list, description="Era/decade tags")
    language: list[str] = Field(default_factory=list, description="Language/region tags")
    special: list[str] = Field(
        default_factory=list, description="Special attributes (remix, acoustic, soundtrack, etc.)"
    )


class PlaylistTagsCategorized(BaseModel):
    tags: list[str] = Field(..., description="Flat list of all tags merged across categories")
    by_category: TagCategories = Field(..., description="Structured tags grouped by category")
    sources: list[str] | None = Field(
        None, description="Up to 3 credible URLs consulted if internet search was needed"
    )


# --------- Prompt + Parser ---------
parser = JsonOutputParser(pydantic_object=PlaylistTagsCategorized)

SYSTEM = """You are an intelligent music tagging assistant.
Your job is to generate concise, reusable playlist tags for a single track.

Grounding & Web:
- If you are not familiar with the song based on the provided metadata,
  SEARCH THE INTERNET for high-confidence context (genre, mood, era, language,
  soundtrack usage, remix/cover info).
- Prefer reliable sources (official pages, well-known music services, reputable databases).
- If credible info is unavailable, use conservative inference from metadata only.
  Do not hallucinate.

Tagging Policy:
- Focus on tags that help sorting into playlists:
  1) Genre/Sub-genre
  2) Mood/Emotion
  3) Context/Use-case
  4) Era/Decade
  5) Language/Region
  6) Special Attributes (e.g., Remix, Acoustic, Duet, Soundtrack, Evergreen, Dance)
- Tags must be short (1–3 words), timeless, and platform-agnostic.
- Do NOT repeat the song title or artist names.
- Use American English unless the language tag itself differs (e.g., “Hindi”).
- If unknown after search, use "Unknown" for that category or omit if your schema allows.

Output:
- Return ONLY what {format_instructions} specifies. No extra text or commentary.
"""

USER = """Generate playlist tags for the following song.

Inputs:
- Song JSON: {song_json}

Constraints:
- Produce between {min_tags} and {max_tags} total tags, prioritizing usefulness
  for playlist sorting.
- Avoid near-duplicates (e.g., "Romance" vs "Romantic"; pick one).
- Prefer broadly recognizable tags over hyper-niche labels unless strongly
  justified by evidence.
- If you used the web, include up to 3 distinct source URLs (credible pages
  only) as allowed by {format_instructions}.

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
    song_json: str,
    min_tags: int = 3,
    max_tags: int = 8,
    backend: str = "openai",
    model: str = "gpt-5-mini",
    temperature: float = 1,
) -> PlaylistTagsCategorized:
    """
    Returns a PlaylistTagsCategorized pydantic object with structured results.
    """
    chain = build_playlist_chain(backend=backend, model=model, temperature=temperature)
    return chain.invoke(
        {
            "song_json": song_json,
            "min_tags": min_tags,
            "max_tags": max_tags,
        }
    )


if __name__ == "__main__":
    yt = YTMusic(
        "oauth.json",
        oauth_credentials=OAuthCredentials(
            client_id=os.getenv("YT_API_CLIENT_ID"), client_secret=os.getenv("YT_API_CLIENT_SECRET")
        ),
    )
    playlist = yt.get_playlist(PLAYLIST_ID)
    title = playlist["title"]
    description = playlist["description"]
    print(f"Title: {title}")
    print(f"Description: {description}")
    tracks = playlist["tracks"]
    sample_tracks = tracks[:5]
    for track in sample_tracks:
        title = track["title"]
        album = track["album"]["name"]
        artists = ", ".join([artist["name"] for artist in track["artists"]])
        print(f"Title: {title}")
        print(f"Album: {album}")
        print(f"Artists: {artists}")
        tags = suggest_playlist_names(json.dumps(track), min_tags=3, max_tags=8)
        print(tags)
