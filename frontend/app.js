const codeInput = document.getElementById("code");
const codeLabel = document.getElementById("code-label");
const languageSelect = document.getElementById("language");
const inputField = document.getElementById("input");
const expectedOutputField = document.getElementById("expected-output");

const analyzeButton = document.getElementById("analyze-button");

const resultSection = document.getElementById("result-section");
const statusElement = document.getElementById("status");
const statusIndicator = document.getElementById("status-indicator");
const statusDescription = document.getElementById("status-description");

const expectedResult = document.getElementById("expected-result");
const actualResult = document.getElementById("actual-result");

const aiSection = document.getElementById("ai-section");
const explanationElement = document.getElementById("explanation");


analyzeButton.addEventListener("click", analyzeCode);
languageSelect.addEventListener("change", updateLanguageUI);


function updateLanguageUI() {
    const language = languageSelect.value;

    if (language === "python") {
        codeLabel.textContent = "Python Code";
        codeInput.placeholder = "Paste your Python code here...";
    } else {
        codeLabel.textContent = "C++ Code";
        codeInput.placeholder = "Paste your C++ code here...";
    }
}


async function analyzeCode() {
    const code = codeInput.value.trim();
    const language = languageSelect.value;
    const input = inputField.value;
    const expectedOutput = expectedOutputField.value.trim();

    if (!code) {
        alert("Please enter your code.");
        return;
    }

    if (!expectedOutput) {
        alert("Please enter the expected output.");
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    resultSection.classList.add("hidden");
    aiSection.classList.add("hidden");

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    code: code,
                    language: language,
                    input: input,
                    expected_output: expectedOutput
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Something went wrong."
            );
        }

        showResult(result);

    } catch (error) {
        alert("Could not connect to the backend.");
        console.error(error);

    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Code";
    }
}


function showResult(result) {
    resultSection.classList.remove("hidden");

    const statusText = result.status.replaceAll("_", " ").toUpperCase();

    statusElement.textContent = statusText;

    const descriptions = {
        passed: "Your program produced the expected output.",
        wrong_answer: "Your program ran successfully, but the output was incorrect.",
        compile_error: "Your program could not be compiled.",
        runtime_error: "Your program crashed while running.",
        timeout: "Your program took too long to finish."
    };

    statusDescription.textContent =
        descriptions[result.status] || "The program execution failed.";

    statusIndicator.className = "";

    if (result.status === "passed") {
        statusIndicator.classList.add("status-success");
    } else if (result.status === "timeout") {
        statusIndicator.classList.add("status-warning");
    } else {
        statusIndicator.classList.add("status-error");
    }

    expectedResult.textContent = result.expected_output || "";
    actualResult.textContent = result.actual_output || "";

    if (result.explanation) {
        aiSection.classList.remove("hidden");

        explanationElement.innerHTML = `
            <div class="explanation-block">
                <h3>What went wrong</h3>
                <p>${result.explanation.what_went_wrong}</p>
            </div>

            <div class="explanation-block">
                <h3>Why it happened</h3>
                <p>${result.explanation.why_it_happened}</p>
            </div>

            <div class="explanation-block">
                <h3>Responsible code</h3>
                <pre>${result.explanation.responsible_code}</pre>
            </div>
        `;
    } else {
        aiSection.classList.add("hidden");
        explanationElement.innerHTML = "";
    }
}