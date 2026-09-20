from engine.ai.models import DebugContext
from engine.ai.openrouter_provider import OpenRouterProvider


context = DebugContext(
    code="""
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;

    cout << a - b;
}
""",
    language="cpp",
    input_data="5 3",
    expected_output="8",
    actual_output="2",
    status="wrong_answer",
    stderr=""
)


provider = OpenRouterProvider()

result = provider.explain_failure(context)

print("\n===== AI DEBUG EXPLANATION =====\n")
print(result.explanation)