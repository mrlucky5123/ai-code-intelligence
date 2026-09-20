from typing import Protocol

from engine.ai.models import DebugContext, DebugExplanation


class AIProvider(Protocol):

    def explain_failure(
        self,
        context: DebugContext
    ) -> DebugExplanation:
        ...