import streamlit as st
from app.services.quota_service import QuotaService

from app.config import constants
from app.config.llm_providers import (
    LLM_PROVIDERS,
    DEFAULT_LLM,
)
from app.services.history_service import HistoryService

config = LLM_PROVIDERS[DEFAULT_LLM]



def render_subsection(title: str, value: str, divider: bool = False):
    st.markdown(f"**{title}**")
    st.caption(value)

    if divider:
        st.divider()


def render_sidebar():
    with st.sidebar:

        # =====================================================
        # Search History
        # =====================================================

        st.markdown("<br>", unsafe_allow_html=True)

        history = HistoryService.get_recent(limit=10)

        with st.expander(
            f"🕒 Search History ({len(history)})",
            expanded=False,
        ):

            if not history:
                st.caption("No searches yet.")

            else:

                for item in reversed(history):

                    query = (
                        item.query
                        if len(item.query) <= 45
                        else item.query[:45] + "..."
                    )

                    if st.button(
                        query,
                        key=f"history_{item.id}",
                        use_container_width=True,
                    ):
                        st.session_state.search_query = item.query
                        st.session_state.current_answer = item.answer
                        st.rerun()

                    st.caption(
                        item.timestamp.strftime("%d %b • %I:%M %p")
                    )

        # =====================================================
        # Free Search Quota
        # =====================================================

        usage = QuotaService.get_usage()
        remaining = QuotaService.remaining()

        st.markdown("**Free Search Quota**")

        if st.session_state.use_app_keys:
            st.progress(
                usage / QuotaService.FREE_LIMIT,
                text=f"{remaining} of {QuotaService.FREE_LIMIT} free searches remaining",
            )

            if QuotaService.is_limit_reached():
                st.error("Free quota exhausted.")
            else:
                st.caption(
                    f"Using App Keys • {usage}/{QuotaService.FREE_LIMIT} searches used"
                )

        else:
            st.success("Unlimited searches with your own API key.")

        # =====================================================
        # Clear History
        # =====================================================

        if history:

            if st.button(
                "🗑️ Clear History",
                use_container_width=True,
            ):
                HistoryService.clear()
                st.rerun()

        # =====================================================
        # Configuration
        # =====================================================

        st.header("⚙️ Configuration")
        st.divider()

        render_subsection("Mode", "🟢 Demo")
        render_subsection("Provider", DEFAULT_LLM.capitalize())
        render_subsection("Model", config["model"])

        st.divider()

        # =====================================================
        # Session State
        # =====================================================

        if "use_app_keys" not in st.session_state:
            st.session_state.use_app_keys = True

        if "gemini_api_key" not in st.session_state:
            st.session_state.gemini_api_key = ""

        if "groq_api_key" not in st.session_state:
            st.session_state.groq_api_key = ""

        # =====================================================
        # API Mode
        # =====================================================

        api_mode = st.radio(
            "API Mode",
            (
                "Use App Keys",
                "Use My Keys",
            ),
            index=0 if st.session_state.use_app_keys else 1,
        )

        st.session_state.use_app_keys = (
            api_mode == "Use App Keys"
        )

        if not st.session_state.use_app_keys:

            st.text_input(
                "Gemini API Key",
                type="password",
                key="gemini_api_key",
            )

            st.text_input(
                "Groq API Key",
                type="password",
                key="groq_api_key",
            )

        st.divider()

        # =====================================================
        # Application Info
        # =====================================================

        render_subsection("Search Provider", "Tavily")
        render_subsection("LLM Gateway", "Portkey")
        render_subsection("Observability", "Logfire")
        render_subsection("Version", constants.APP_VERSION)

        