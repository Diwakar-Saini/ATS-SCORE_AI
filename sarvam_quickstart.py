import os
from pathlib import Path

from sarvamai import SarvamAI


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def extract_text(response) -> str:
    choices = getattr(response, "choices", None) or []
    if choices:
        message = getattr(choices[0], "message", None)
        content = getattr(message, "content", None)
        if isinstance(content, str) and content.strip():
            return content.strip()
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text") or item.get("content")
                else:
                    text = getattr(item, "text", None) or getattr(item, "content", None)
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
            if parts:
                return "\n".join(parts)
    return str(response)


def main() -> None:
    load_env_file(Path(__file__).resolve().parent / ".env")
    api_key = os.environ.get("SARVAM_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Missing SARVAM_API_KEY. Add it to .env and run again.")

    client = SarvamAI(api_subscription_key=api_key)
    response = client.chat.completions(
        model="sarvam-105b-conversations",
        messages=[
            {"role": "user", "content": "Say hello in one short sentence."}
        ],
    )
    print(extract_text(response))


if __name__ == "__main__":
    main()
