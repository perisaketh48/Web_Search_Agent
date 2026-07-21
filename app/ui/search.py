import streamlit as st

from app.agent.agent import SearchAgent
from app.schemas.credentials import Credentials
from app.schemas.search_history import SearchHistory
from app.services.history_service import HistoryService
from app.services.quota_service import QuotaService

agent = SearchAgent()

# -----------------------------------------------------
# Initialize Services
# -----------------------------------------------------

HistoryService.initialize()
QuotaService.initialize()

# -----------------------------------------------------
# Session State Initialization
# -----------------------------------------------------

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "current_answer" not in st.session_state:
    st.session_state.current_answer = ""

if "current_sources" not in st.session_state:
    st.session_state.current_sources = []


def render_search():
    st.subheader("🔍 Search the Web")
    st.caption("Ask anything and get source-backed answers.")

    # -----------------------------------------------------
    # Search Input
    # -----------------------------------------------------

    search_query = st.text_input(
        "Search",
        key="search_query",
        placeholder="Ask a question...",
    )

    search_clicked = st.button(
        "Search",
        icon=":material/search:",
    )

    # -----------------------------------------------------
    # Run Search
    # -----------------------------------------------------

    if search_clicked:

        if not search_query.strip():
            st.warning("Please enter your query.")
            return

        # -------------------------------------------------
        # Free Quota Check
        # -------------------------------------------------

        if (
            st.session_state.use_app_keys
            and QuotaService.is_limit_reached()
        ):
            st.error(
                "You have used all 3 free searches.\n\n"
                "Please switch to **'Use My Keys'** in the sidebar "
                "and provide your Gemini or Groq API key."
            )
            return

        try:

            with st.spinner("Thinking..."):

                credentials = Credentials(
                    use_app_keys=st.session_state.use_app_keys,
                    gemini_api_key=st.session_state.gemini_api_key,
                    groq_api_key=st.session_state.groq_api_key,
                )

                final_state = agent.run_agent(
                    query=search_query,
                    credentials=credentials,
                )


            # -------------------------------------------------
            # Successful Search
            # -------------------------------------------------

            if st.session_state.use_app_keys:
                QuotaService.increment()

            # Save answer
            st.session_state.current_answer = final_state.final_answer

            # Save sources
            st.session_state.current_sources = final_state.search_results

            # Save search history
            history = SearchHistory(
                query=search_query,
                answer=final_state.final_answer,
            )

            HistoryService.add(history)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # -----------------------------------------------------
    # Display Answer
    # -----------------------------------------------------

    if st.session_state.current_answer:

        st.markdown("### 💬 Answer")
        st.write(st.session_state.current_answer)

        # -------------------------------------------------
        # Display Sources
        # -------------------------------------------------

        if st.session_state.current_sources:

            st.markdown("### 📚 Sources")

            for source in st.session_state.current_sources:

                st.markdown(
                    f"- [{source.title}]({source.url})"
                )

        st.markdown(
"""
    <div style='text-align: center; color: gray; font-size: 14px; line-height: 1.6;'>
        <p>© 2026 Web Search Agent | Designed and Developed By Saketh</p>
        <p style='margin-top: 15px;'>
            <strong>🟡 Session History:</strong> Your searches are stored only while this browser tab is open.<br>
            Refreshing or closing the tab will clear your search history.
        </p>
        
    </div>
    """,  
    unsafe_allow_html=True
)