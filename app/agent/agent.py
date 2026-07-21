from app.agent.graph import graph
from app.agent.state import AgentState
from app.schemas.credentials import Credentials



class SearchAgent:

    def run_agent(
        self,
        query: str,
        credentials: Credentials,
    ) -> AgentState:

        initial_state = AgentState(
            query=query,
            credentials=credentials,
        )

        result = graph.invoke(initial_state)

        return AgentState.model_validate(result)