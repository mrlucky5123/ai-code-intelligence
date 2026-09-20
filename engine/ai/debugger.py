from engine.ai.models import DebugContext, DebugExplanation
from engine.ai.provider import AIProvider


class AIDebugger:

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def explain_failure(
        self,
        context: DebugContext
    ) -> DebugExplanation:

        return self.provider.explain_failure(context)