from dataclasses import dataclass

from openai import OpenAI


@dataclass
class LLMClient:
    client: OpenAI
    use_portkey: bool