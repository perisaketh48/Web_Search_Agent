import streamlit as st


class QuotaService:

    SESSION_KEY = "search_count"
    FREE_LIMIT = 3

    @classmethod
    def initialize(cls) -> None:
        if cls.SESSION_KEY not in st.session_state:
            st.session_state[cls.SESSION_KEY] = 0

    @classmethod
    def increment(cls) -> None:
        cls.initialize()
        st.session_state[cls.SESSION_KEY] += 1

    @classmethod
    def get_usage(cls) -> int:
        cls.initialize()
        return st.session_state[cls.SESSION_KEY]

    @classmethod
    def remaining(cls) -> int:
        cls.initialize()
        return max(0, cls.FREE_LIMIT - cls.get_usage())

    @classmethod
    def is_limit_reached(cls) -> bool:
        cls.initialize()
        return cls.get_usage() >= cls.FREE_LIMIT

    @classmethod
    def reset(cls) -> None:
        st.session_state[cls.SESSION_KEY] = 0