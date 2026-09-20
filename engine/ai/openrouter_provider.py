import os
from urllib import response

from dotenv import load_dotenv
from openai import OpenAI

from engine.ai.models import DebugContext, DebugExplanation


load_dotenv()


class OpenRouterProvider:

    def __init__(
        self,
        model: str = "openrouter/free"
    ):

        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        self.model = model

    def explain_failure(
        self,
        context: DebugContext
    ) -> DebugExplanation:

        prompt = f"""
You are an AI debugging assistant for C++.

Analyze the following failed program execution.

Status:
{context.status}

Code:
```cpp
{context.code}

Input:
{context.input_data}

Expected output:
{context.expected_output}

Actual output:
{context.actual_output}

Compiler/runtime error:
{context.stderr}

Explain:

What went wrong.
Why the program produced the observed result.
What part of the code is likely responsible.

Do not rewrite the entire program.
Do not invent information that is not supported by the evidence.
Keep the explanation concise and technically accurate.
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        return DebugExplanation(
            explanation=response.choices[0].message.content
        )