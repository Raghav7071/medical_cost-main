import streamlit as st

from repositories.sessions import delete_session, resolve_session

_DEFAULTS = {
    "user_id": None,
    "username": None,
    "session_token": None,
    "prediction_history": [],
    "page": "dashboard",
    "show_auth": False,
}


def init_state() -> None:
    """Seed default keys, then rehydrate auth from a `?session=<token>` query
    param if present. Runs on every page load."""
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Already authenticated in this Streamlit session — nothing to do.
    if st.session_state["user_id"]:
        return

    token = st.query_params.get("session")
    if not token:
        return

    found = resolve_session(token)
    if not found:
        # Stale or revoked token — strip it from the URL.
        st.query_params.pop("session", None)
        return

    user_id, username = found
    st.session_state["user_id"] = user_id
    st.session_state["username"] = username
    st.session_state["session_token"] = token


def remember_session(token: str) -> None:
    """Stash the token in session state and the URL so it survives reload."""
    st.session_state["session_token"] = token
    st.query_params["session"] = token


def clear_auth() -> None:
    token = st.session_state.get("session_token")
    if token:
        delete_session(token)
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.query_params.pop("session", None)
