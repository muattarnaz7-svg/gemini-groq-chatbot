import os
import time
from collections.abc import Iterator

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
import groq

load_dotenv()

PROVIDERS = ["Gemini", "Groq"]

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

SYSTEM_PROMPT = (
    "You are a helpful, friendly assistant. "
    "Reply in the same language the user writes in. "
    "Keep answers clear and simple."
)
MAX_TOKENS = 1000
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 2

# Dono providers ke API errors, taake CLI/app ek hi jagah catch kar sake
API_ERRORS = (errors.APIError, groq.APIError)


def create_client(provider: str = "Gemini"):
    if provider == "Gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set in your .env file.")
        return genai.Client(api_key=api_key)

    if provider == "Groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in your .env file.")
        return groq.Groq(api_key=api_key)

    raise RuntimeError(f"Unknown provider: {provider}")


def stream_reply(
    client,
    messages: list[dict[str, str]],
    system_prompt: str,
    provider: str = "Gemini",
) -> Iterator[str]:
    if provider == "Groq":
        yield from _stream_groq(client, messages, system_prompt)
    else:
        yield from _stream_gemini(client, messages, system_prompt)


def _stream_gemini(client, messages, system_prompt) -> Iterator[str]:
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
                model=GEMINI_MODEL,
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


def _stream_groq(client, messages, system_prompt) -> Iterator[str]:
    full_messages = [{"role": "system", "content": system_prompt}, *messages]

    for attempt in range(MAX_RETRIES + 1):
        sent_text = False
        try:
            stream = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=full_messages,
                max_completion_tokens=MAX_TOKENS,
                reasoning_effort="low",  # gpt-oss soch mein token kam kharch kare
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                text = chunk.choices[0].delta.content
                if text:
                    sent_text = True
                    yield text
            return
        except groq.APIStatusError as exc:
            if exc.status_code not in (429, 503) or sent_text or attempt == MAX_RETRIES:
                raise
            time.sleep(RETRY_DELAY_SECONDS * (2**attempt))