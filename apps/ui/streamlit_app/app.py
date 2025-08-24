import os

import streamlit as st
from redis import Redis
from sortune_adapters.storage.redis_repo import RedisPlaylistRepo
from sortune_adapters.ytmusic.client import YTMusicClient
from sortune_core.rules.simple import ByTitle

# ---- Config ----
st.set_page_config(page_title="Sortune", layout="centered")
st.title("🎶 Sortune — Playlist Manager (Demo)")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = Redis.from_url(REDIS_URL)
repo = RedisPlaylistRepo(r)


# ---- Helpers ----
def load_playlist(pid: str) -> None:
    st.session_state["pl"] = repo.get(pid)


def seed_demo(pid: str = "demo") -> dict:
    """
    Idempotent seeding of a demo playlist. Does not require the worker package.
    """
    pl = repo.get(pid)
    if not pl.tracks:
        pl.name = "Demo Playlist"
        pl.tracks = YTMusicClient().sample_tracks()
        repo.save(pl)
    return {"playlist": pl.id, "tracks": len(pl.tracks)}


# ---- UI ----
with st.sidebar:
    st.subheader("Settings")
    st.caption(f"Redis: `{REDIS_URL}`")
    st.markdown("---")
    st.write("Quick Actions")
    if st.button("🧪 Seed demo playlist"):
        res = seed_demo("demo")
        st.success(f"Seeded {res['tracks']} tracks into playlist '{res['playlist']}'")

pid = st.text_input("Playlist ID", value=st.session_state.get("current_pid", "demo"))
cols = st.columns(3)
with cols[0]:
    if st.button("Load playlist"):
        st.session_state["current_pid"] = pid
        load_playlist(pid)
with cols[1]:
    if st.button("Sort by title"):
        pl = repo.get(pid)
        pl.tracks = list(ByTitle.apply(pl.tracks))
        repo.save(pl)
        st.success("Sorted! Click 'Load playlist' to refresh.")
with cols[2]:
    if st.button("Refresh"):
        load_playlist(pid)

st.markdown("---")

pl = st.session_state.get("pl")
if not pl:
    st.info(
        "No playlist loaded yet. Try **Seed demo playlist** in the sidebar, then click **Load playlist**."
    )
else:
    st.subheader(pl.name or pid)
    if not pl.tracks:
        st.warning("Playlist has no tracks.")
    else:
        for t in pl.tracks:
            artists = ", ".join(a.name for a in t.artists)
            st.write(f"- **{t.title}** — {artists}")
