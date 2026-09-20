import os
# from urllib import response

from dotenv import load_dotenv
from google import genai

from engine.ai.models import DebugContext, DebugExplanation


load_dotenv()


class GeminiProvider:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(
            api_key=api_key
        )

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

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return DebugExplanation(
            explanation=response.text
        )