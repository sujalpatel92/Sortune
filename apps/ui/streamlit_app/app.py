import os
from typing import Any

import streamlit as st
from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient
from sortune_core.rules.simple import ByTitle

# ---- Config ----
st.set_page_config(page_title="Sortune", layout="centered")
st.title("🎶 Sortune — Playlist Manager (Demo)")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
YT_OAUTH_PATH = os.getenv("YT_OAUTH_PATH", ".cache/ytmusic_oauth.json")
r = Redis.from_url(REDIS_URL)
repo = RedisPlaylistRepo(r)

# ---- Session init ----
st.session_state.setdefault("pl", None)
st.session_state.setdefault("current_pid", "demo")
st.session_state.setdefault("yt_playlists", [])  # list of {playlistId,title,count,thumbnails}
st.session_state.setdefault("yt_selected_idx", 0)


# ---- Helpers ----
def load_playlist(pid: str) -> None:
    st.session_state["pl"] = repo.get(pid)


def seed_demo(pid: str = "demo") -> dict[str, Any]:
    """
    Idempotent seeding of a demo playlist. Does not require the worker package.
    """
    pl = repo.get(pid)
    if not pl.tracks:
        pl.name = "Demo Playlist"
        pl.tracks = YTMusicClient().sample_tracks()
        repo.save(pl)
    return {"playlist": pl.id, "tracks": len(pl.tracks)}


def import_yt_playlist(
    pid: str, name_hint: str | None = None, limit: int | None = None
) -> dict[str, Any]:
    """
    Import a YT playlist (by id) into Redis under the same id.
    """
    client = YTMusicClient()
    tracks = client.get_playlist_tracks(playlist_id=pid, limit=limit)
    display_name = name_hint or os.getenv("YT_PLAYLIST_NAME") or f"YT:{pid}"
    pl = repo.get(pid)
    pl.name = display_name
    pl.tracks = tracks
    repo.save(pl)
    return {"playlist": pl.id, "tracks": len(pl.tracks), "name": display_name}


# ---- Sidebar ----
with st.sidebar:
    st.subheader("Settings")
    st.caption(f"Redis: `{REDIS_URL}`")
    st.caption(f"YT OAuth file: `{YT_OAUTH_PATH}`")
    st.markdown("---")
    st.write("Quick Actions")
    if st.button("🧪 Seed demo playlist"):
        res = seed_demo("demo")
        st.success(f"Seeded {res['tracks']} tracks into playlist '{res['playlist']}'")


# ---- YT Music (live) ----
with st.expander("YouTube Music (beta) — connect & import", expanded=False):
    st.caption("First run will open a browser for OAuth and save a token under `.cache/`.")
    cols_y = st.columns([1, 1, 2])

    with cols_y[0]:
        if st.button("Connect & List My Playlists"):
            try:
                items = YTMusicClient().list_library_playlists(limit=200)
                st.session_state["yt_playlists"] = items or []
                st.success(f"Fetched {len(items)} playlists from your library.")
            except Exception as e:
                st.error(str(e))

    playlists: list[dict[str, Any]] = st.session_state["yt_playlists"]
    titles = [f"{p.get('title', '(no title)')} • {p.get('count', '?')} tracks" for p in playlists]
    if playlists:
        st.write("Pick a playlist to import into Redis:")
        st.session_state["yt_selected_idx"] = st.selectbox(
            "Library playlists",
            options=list(range(len(playlists))),
            index=min(st.session_state.get("yt_selected_idx", 0), max(0, len(playlists) - 1)),
            format_func=lambda i: titles[i],
        )
        sel = playlists[st.session_state["yt_selected_idx"]]
        pick_cols = st.columns([1, 1])
        with pick_cols[0]:
            if st.button("Import selected"):
                try:
                    res = import_yt_playlist(
                        pid=sel.get("playlistId", ""),
                        name_hint=sel.get("title") or None,
                    )
                    st.success(
                        f"Imported {res['tracks']} tracks into '{res['name']}' ({res['playlist']})."
                    )
                    st.session_state["current_pid"] = res["playlist"]
                except Exception as e:
                    st.error(str(e))
        with pick_cols[1]:
            if st.button("Load selected into view"):
                st.session_state["current_pid"] = sel.get("playlistId", "")
                load_playlist(st.session_state["current_pid"])

    st.markdown("---")
    st.caption("Know the ID already?")
    cols_id = st.columns([2, 1, 1])
    with cols_id[0]:
        yt_id_manual = st.text_input(
            "YouTube Music playlist ID", value=os.getenv("YT_PLAYLIST_ID", "")
        )
    with cols_id[1]:
        if st.button("Import by ID"):
            if yt_id_manual:
                try:
                    res = import_yt_playlist(pid=yt_id_manual)
                    st.success(
                        f"Imported {res['tracks']} tracks into '{res['name']}' ({res['playlist']})."
                    )
                    st.session_state["current_pid"] = res["playlist"]
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("Provide a playlist ID.")
    with cols_id[2]:
        if st.button("Load by ID"):
            if yt_id_manual:
                st.session_state["current_pid"] = yt_id_manual
                load_playlist(yt_id_manual)
            else:
                st.warning("Provide a playlist ID.")


# ---- Main controls ----
pid = st.text_input("Playlist ID", value=st.session_state.get("current_pid", "demo"))
cols = st.columns(3)
with cols[0]:
    if st.button("Load playlist"):
        st.session_state["current_pid"] = pid
        load_playlist(pid)
with cols[1]:
    if st.button("Sort by title"):
        pl = repo.get(pid)
        if not pl or not pl.tracks:
            st.warning("No tracks to sort.")
        else:
            pl.tracks = list(ByTitle.apply(pl.tracks))
            repo.save(pl)
            st.success("Sorted! Click 'Load playlist' to refresh.")
with cols[2]:
    if st.button("Refresh"):
        load_playlist(pid)

st.markdown("---")

# ---- Playlist view ----
pl = st.session_state.get("pl")
if not pl:
    st.info(
        "No playlist loaded yet. Try **Seed demo playlist** in the sidebar, "
        "or use the **YouTube Music** expander to import one, then click **Load playlist**."
    )
else:
    st.subheader(pl.name or pid)
    if not pl.tracks:
        st.warning("Playlist has no tracks.")
    else:
        for t in pl.tracks:
            artists = ", ".join(a.name for a in t.artists)
            st.write(f"- **{t.title}** — {artists}")
