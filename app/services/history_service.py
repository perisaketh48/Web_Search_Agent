import streamlit as st

from app.schemas.search_history import SearchHistory


class HistoryService:

    SESSION_KEY = "search_history"

    @classmethod
    def initialize(cls):
        if cls.SESSION_KEY not in st.session_state:
            st.session_state[cls.SESSION_KEY] = []

    @classmethod
    def add(cls, history: SearchHistory):
        cls.initialize()
        st.session_state[cls.SESSION_KEY].append(history)

    @classmethod
    def get_all(cls) -> list[SearchHistory]:
        cls.initialize()
        return st.session_state[cls.SESSION_KEY]

    @classmethod
    def get_recent(
        cls,
        limit: int = 10,
    ) -> list[SearchHistory]:
        cls.initialize()
        return st.session_state[cls.SESSION_KEY][-limit:]



    @classmethod
    def clear(cls):
        st.session_state[cls.SESSION_KEY] = []