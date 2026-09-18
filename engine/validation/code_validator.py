SUPPORTED_LANGUAGES = {"cpp"}

def validate_code(code: str, language: str) -> tuple[bool,str]:
    if not code.strip():
        return False, "Code cannot be empty."

    if language.lower() not in SUPPORTED_LANGUAGES:
        return False, f"Unsupported language: {language}"

    return True, "Code is valid."