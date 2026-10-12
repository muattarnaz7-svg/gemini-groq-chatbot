import os
import time
from collections.abc import Iterator

from google import genai
from google.genai import errors, types
from dotenv import load_dotenv 

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
SYSTEM_PROMPT = (
    "You are a helpful, friendly assistant. "
    "Reply in the same language the user writes in. "
    "Keep answers clear and simple."
)
MAX_TOKENS = 1000
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1


def create_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add a rotated key to your .env file or environment."
        )
    return genai.Client(api_key=api_key)


def stream_reply(
    client: genai.Client,
    messages: list[dict[str, str]],
    system_prompt: str,
) -> Iterator[str]:
    contents = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
    ]

    for attempt in range(MAX_RETRIES + 1):
        sent_text = False
        try:
            response = client.models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=MAX_TOKENS,
                ),
            )
            for chunk in response:
                if chunk.text:
                    sent_text = True
                    yield chunk.text
            return
        except errors.APIError as exc:
            if exc.code != 503 or sent_text or attempt == MAX_RETRIES:
                raise
            time.sleep(RETRY_DELAY_SECONDS * (2**attempt))