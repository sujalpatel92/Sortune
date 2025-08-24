import json
import os
from typing import Any

from dotenv import load_dotenv
from ytmusicapi import OAuthCredentials, YTMusic

load_dotenv()


def write_to_cache(cache_file_name: str, data: list[dict[str, Any]]):
    if not data:
        return
    filepath = os.path.join("cache", cache_file_name)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def get_from_cache(cache_file_name: str) -> list[dict[str, Any]]:
    if not os.path.exists(os.path.join("cache", cache_file_name)):
        return None
    filepath = os.path.join("cache", cache_file_name)
    with open(filepath) as f:
        return json.load(f)


def get_playlists_of_interest(playlists: list[dict[str, Any]]):
    if not playlists:
        return None

    playlists_of_interest = []
    for playlist in playlists:
        if "author" in playlist and playlist["author"] != "YouTube Music":
            playlists_of_interest.append(playlist)
        if "author" not in playlist:
            playlists_of_interest.append(playlist)
    return playlists_of_interest


if __name__ == "__main__":
    yt = YTMusic(
        "oauth.json",
        oauth_credentials=OAuthCredentials(
            client_id=os.getenv("YT_API_CLIENT_ID"), client_secret=os.getenv("YT_API_CLIENT_SECRET")
        ),
    )

    playlists = get_from_cache("playlists.json")
    if not playlists:
        playlists = yt.get_library_playlists()
        playlists_of_interest = get_playlists_of_interest(playlists)
        write_to_cache("playlists.json", playlists_of_interest)

    for playlist in playlists:
        print(playlist)

    albums = get_from_cache("albums.json")
    if not albums:
        albums = yt.get_library_albums()
        write_to_cache("albums.json", albums)

    for album in albums:
        print(album)

    artists = get_from_cache("artists.json")
    if not artists:
        artists = yt.get_library_artists()
        write_to_cache("artists.json", artists)

    for artist in artists:
        print(artist)
