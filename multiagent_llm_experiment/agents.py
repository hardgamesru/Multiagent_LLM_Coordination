from __future__ import annotations

from dataclasses import dataclass

from llm_client import BaseLLMClient
from prompts import (
    ANALYST_SYSTEM_PROMPT,
    DEVELOPER_SYSTEM_PROMPT,
    MANAGER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    TESTER_SYSTEM_PROMPT,
)


@dataclass
class AgentResponse:
    agent_name: str
    role: str
    content: str
    messages_used: int


class BaseAgent:
    def __init__(self, name: str, role: str, llm_client: BaseLLMClient, system_prompt: str) -> None:
        self.name = name
        self.role = role
        self.llm_client = llm_client
        self.system_prompt = system_prompt

    def run(self, input_text: str) -> AgentResponse:
        content = self.llm_client.generate(self.system_prompt, input_text)
        return AgentResponse(
            agent_name=self.name,
            role=self.role,
            content=content,
            messages_used=1,
        )


class AnalystAgent(BaseAgent):
    def __init__(self, llm_client: BaseLLMClient) -> None:
        super().__init__("analyst", "Analyst", llm_client, ANALYST_SYSTEM_PROMPT)


class DeveloperAgent(BaseAgent):
    def __init__(self, llm_client: BaseLLMClient, name: str = "developer") -> None:
        super().__init__(name, "Developer", llm_client, DEVELOPER_SYSTEM_PROMPT)


class TesterAgent(BaseAgent):
    def __init__(self, llm_client: BaseLLMClient) -> None:
        super().__init__("tester", "Tester", llm_client, TESTER_SYSTEM_PROMPT)


class ReviewerAgent(BaseAgent):
    def __init__(self, llm_client: BaseLLMClient) -> None:
        super().__init__("reviewer", "Reviewer", llm_client, REVIEWER_SYSTEM_PROMPT)


class ManagerAgent(BaseAgent):
    def __init__(self, llm_client: BaseLLMClient) -> None:
        super().__init__("manager", "Manager", llm_client, MANAGER_SYSTEM_PROMPT)
